"""
Fitness Tracking Eye - Dual-View Video Simulator & Multi-Camera Fusion Engine
=============================================================================
Skrip simulator sinkronisasi dua sudut pandang (Dual-View / Multi-Camera):
1. Membaca dua sumber video:
   - PV1: POV Kamera Depan (Frontal View)
   - PV2: POV Kamera Samping (Sagittal View)
2. Otomatis memuat video default per jenis latihan dari data/videos/:
   - Push Up     : PushUpPV1.mp4 & PushUpPV2.mp4
   - Sit Up      : SitUpPV1.mp4 & SitUpPV2.mp4
   - Squat Jump  : SquatJumpPV1.mp4 & SquatJumpPV2.mp4
   - Vert Jump   : VertJumpPV1.mp4 & VertJumpPV2.mp4
3. Menyelaraskan garis waktu (temporal sync) via offset timestamp (--start1 & --start2).
4. Pacing real-time 1.0x terkunci ke jam dinding (wall-clock) dengan kompensasi AI delay.
5. Menjalankan estimasi pose 3D independen untuk kedua kamera via MediaPipe BlazePose.
6. Fusi Biomekanik Multi-Sudut:
   - Sagittal (PV2) : Sudut siku, kelurusan tulang punggung (hip sag), sudut lutut, penghitung repetisi.
   - Frontal (PV1)  : Simetri kemiringan bahu (shoulder tilt), bukaan tangan (hand width), knee valgus.
7. Tampilan Side-by-Side cerdas (mendukung penuh video Portrait 1080x1920 dan Landscape).
8. Kontrol live hotkeys interaktif: '[' / ']' untuk geser offset 0.1s saat video berjalan.
9. Siaran data skeleton terpadu via WebSocket (ws://localhost:8765).
"""

import cv2
import mediapipe as mp
import numpy as np
import yaml
import json
import time
import argparse
import asyncio
import threading
from pathlib import Path

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

DEFAULT_EXERCISE_VIDEOS = {
    "push_up": ("data/videos/PushUpPV1.mp4", "data/videos/PushUpPV2.mp4"),
    "sit_up": ("data/videos/SitUpPV1.mp4", "data/videos/SitUpPV2.mp4"),
    "squat_jump": ("data/videos/SquatJumpPV1.mp4", "data/videos/SquatJumpPV2.mp4"),
    "vertical_jump": ("data/videos/VertJumpPV1.mp4", "data/videos/VertJumpPV2.mp4"),
}


class DualViewExerciseTracker:
    """Mesin evaluasi fusi biomekanik multi-sudut (Sagittal/PV2 + Frontal/PV1)."""
    def __init__(self, config_path="config/exercise_config.yaml", exercise_name="push_up"):
        self.exercise_name = exercise_name
        self.counter = 0
        self.stage = "UP"  # "UP" or "DOWN"
        self.last_transition_time = time.time()
        self.min_transition_sec = 0.35  # Anti-jitter debounce filter
        self.form_errors = []
        self.sagittal_angles = {}
        self.frontal_metrics = {}
        self.config = self._load_config(config_path)

        # State tracking khusus vertical jump
        self.vjump_baseline_y = None
        self.vjump_max_height_px = 0.0

    def _load_config(self, config_path):
        cfg_file = Path(config_path)
        if cfg_file.exists():
            with open(cfg_file, "r") as f:
                return yaml.safe_load(f)
        return {}

    @staticmethod
    def calculate_angle(a, b, c):
        """Menghitung sudut 2D (derajat) antara titik A, B, C dengan vertex di B."""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360.0 - angle
        return float(angle)

    def process_dual_landmarks(self, lms_frontal, lms_sagittal):
        """
        Fusi metrik biomekanik:
        - lms_sagittal (PV2 / Samping): Sudut sendi fleksi-ekstensi & state machine repetisi
        - lms_frontal  (PV1 / Depan)  : Keseimbangan simetri bahu & bukaan tangan / posisi lutut
        """
        self.form_errors = []
        self.sagittal_angles = {}
        self.frontal_metrics = {}
        now = time.time()

        # =================================================================
        # 1. EVALUASI KAMERA SAMPING (SAGITTAL / PV2)
        # =================================================================
        if lms_sagittal is not None:
            # Auto-detect profil tubuh (Kiri vs Kanan) berdasarkan visibilitas sendi
            l_vis = (lms_sagittal[11].visibility + lms_sagittal[13].visibility + lms_sagittal[23].visibility) / 3.0
            r_vis = (lms_sagittal[12].visibility + lms_sagittal[14].visibility + lms_sagittal[24].visibility) / 3.0
            use_left = l_vis >= r_vis

            sh = [lms_sagittal[11 if use_left else 12].x, lms_sagittal[11 if use_left else 12].y]
            el = [lms_sagittal[13 if use_left else 14].x, lms_sagittal[13 if use_left else 14].y]
            wr = [lms_sagittal[15 if use_left else 16].x, lms_sagittal[15 if use_left else 16].y]
            hp = [lms_sagittal[23 if use_left else 24].x, lms_sagittal[23 if use_left else 24].y]
            kn = [lms_sagittal[25 if use_left else 26].x, lms_sagittal[25 if use_left else 26].y]
            ak = [lms_sagittal[27 if use_left else 28].x, lms_sagittal[27 if use_left else 28].y]

            # A. PUSH UP
            if self.exercise_name == "push_up":
                elbow_angle = self.calculate_angle(sh, el, wr)
                body_angle = self.calculate_angle(sh, hp, ak)
                self.sagittal_angles["Elbow Angle"] = round(elbow_angle, 1)
                self.sagittal_angles["Body Line"] = round(body_angle, 1)

                cfg = self.config.get("push_up", {})
                up_th = cfg.get("elbow_angle", {}).get("up_threshold", 155)
                down_th = cfg.get("elbow_angle", {}).get("down_threshold", 95)

                if elbow_angle < down_th and self.stage != "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "DOWN"
                        self.last_transition_time = now
                elif elbow_angle > up_th and self.stage == "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "UP"
                        self.counter += 1
                        self.last_transition_time = now

                # Form check: Punggung melengkung / hip sag
                if body_angle < 150:
                    self.form_errors.append("Punggung Melengkung (Sagittal)")

            # B. SQUAT / SQUAT JUMP
            elif "squat" in self.exercise_name:
                knee_angle = self.calculate_angle(hp, kn, ak)
                self.sagittal_angles["Knee Angle"] = round(knee_angle, 1)

                cfg = self.config.get("squat_jump", {})
                stand_th = cfg.get("knee_angle", {}).get("stand_threshold", 160)
                squat_th = cfg.get("knee_angle", {}).get("squat_threshold", 95)

                if knee_angle < squat_th and self.stage != "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "DOWN"
                        self.last_transition_time = now
                elif knee_angle > stand_th and self.stage == "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "UP"
                        self.counter += 1
                        self.last_transition_time = now

                if kn[0] > ak[0] + 0.06:
                    self.form_errors.append("Lutut Lewati Jari Kaki")

            # C. SIT UP
            elif self.exercise_name == "sit_up":
                hip_angle = self.calculate_angle(sh, hp, kn)
                self.sagittal_angles["Hip Angle"] = round(hip_angle, 1)

                if hip_angle > 130 and self.stage != "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "DOWN"
                        self.last_transition_time = now
                elif hip_angle < 75 and self.stage == "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "UP"
                        self.counter += 1
                        self.last_transition_time = now

            # D. VERTICAL JUMP
            elif "vert" in self.exercise_name:
                knee_angle = self.calculate_angle(hp, kn, ak)
                self.sagittal_angles["Knee Angle"] = round(knee_angle, 1)

                hip_y = hp[1]
                if self.vjump_baseline_y is None:
                    self.vjump_baseline_y = hip_y

                # Crouch -> Jump Takeoff -> Landing
                if knee_angle < 130 and self.stage != "CROUCH":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "CROUCH"
                        self.last_transition_time = now
                elif self.stage == "CROUCH" and hip_y < self.vjump_baseline_y - 0.05:
                    self.stage = "AIRBORNE"
                    self.last_transition_time = now
                elif self.stage == "AIRBORNE" and abs(hip_y - self.vjump_baseline_y) < 0.04:
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "LANDED"
                        self.counter += 1
                        self.last_transition_time = now

        # =================================================================
        # 2. EVALUASI KAMERA DEPAN (FRONTAL / PV1)
        # =================================================================
        if lms_frontal is not None:
            l_sh = [lms_frontal[11].x, lms_frontal[11].y]
            r_sh = [lms_frontal[12].x, lms_frontal[12].y]
            l_wr = [lms_frontal[15].x, lms_frontal[15].y]
            r_wr = [lms_frontal[16].x, lms_frontal[16].y]
            l_kn = [lms_frontal[25].x, lms_frontal[25].y]
            r_kn = [lms_frontal[26].x, lms_frontal[26].y]
            l_ak = [lms_frontal[27].x, lms_frontal[27].y]
            r_ak = [lms_frontal[28].x, lms_frontal[28].y]

            # A. Kemiringan Bahu (Shoulder Tilt)
            dx = abs(r_sh[0] - l_sh[0])
            dy = r_sh[1] - l_sh[1]
            shoulder_tilt_deg = abs(np.arctan2(dy, max(0.001, dx)) * 180.0 / np.pi)
            self.frontal_metrics["Shoulder Tilt"] = f"{round(shoulder_tilt_deg, 1)} deg"

            if shoulder_tilt_deg > 6.5:
                self.form_errors.append("Bahu Miring (Frontal)")

            # B. Rasio Bukaan Tangan vs Bahu (Push Up / Plank)
            if self.exercise_name == "push_up":
                sh_dist = np.hypot(r_sh[0] - l_sh[0], r_sh[1] - l_sh[1])
                wr_dist = np.hypot(r_wr[0] - l_wr[0], r_wr[1] - l_wr[1])
                if sh_dist > 0.05:
                    width_ratio = wr_dist / sh_dist
                    self.frontal_metrics["Hand Width"] = f"{round(width_ratio, 2)}x Bahu"
                    if width_ratio > 2.3:
                        self.form_errors.append("Posisi Tangan Terlalu Lebar")
                    elif width_ratio < 0.75:
                        self.form_errors.append("Posisi Tangan Terlalu Sempit")

            # C. Cek Lutut Masuk ke Dalam (Valgus) untuk Squat / Jump
            if "squat" in self.exercise_name or "vert" in self.exercise_name:
                knee_dist = np.hypot(r_kn[0] - l_kn[0], r_kn[1] - l_kn[1])
                ankle_dist = np.hypot(r_ak[0] - l_ak[0], r_ak[1] - l_ak[1])
                if ankle_dist > 0.05:
                    if knee_dist < ankle_dist * 0.70:
                        self.form_errors.append("Lutut Tertekuk Ke Dalam (Valgus)")

        return self.counter, self.stage, self.sagittal_angles, self.frontal_metrics, self.form_errors


class MockDualWebSocketServer:
    """Server WebSocket untuk menyiarkan fusi koordinat & status 2 kamera sekaligus."""
    def __init__(self, host="0.0.0.0", port=8765):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.latest_payload = None
        self._thread = None
        self._loop = None

    def start(self):
        try:
            import websockets
            self._thread = threading.Thread(target=self._run_server, daemon=True)
            self._thread.start()
            print(f"[WebSocket] Dual-View Server aktif di ws://{self.host}:{self.port}")
        except ImportError:
            print("[WebSocket] Pustaka 'websockets' belum terpasang. Mode broadcast dinonaktifkan.")

    def _run_server(self):
        import websockets
        async def handler(websocket):
            self.connected_clients.add(websocket)
            print(f"[WebSocket] Klien terhubung ke Dual-View Stream! Total: {len(self.connected_clients)}")
            try:
                await websocket.wait_closed()
            finally:
                self.connected_clients.remove(websocket)

        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        
        async def main():
            async with websockets.serve(handler, self.host, self.port):
                while True:
                    if self.latest_payload and self.connected_clients:
                        message = json.dumps(self.latest_payload)
                        websockets.broadcast(self.connected_clients, message)
                    await asyncio.sleep(1 / 30)

        self._loop.run_until_complete(main())

    def broadcast(self, payload):
        self.latest_payload = payload


def draw_glass_card(img, x1, y1, x2, y2, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.75):
    """Menggambar panel HUD semi-transparan via ROI slicing cepat tanpa copy full image."""
    h_img, w_img, _ = img.shape
    x1, y1 = max(0, int(x1)), max(0, int(y1))
    x2, y2 = min(w_img, int(x2)), min(h_img, int(y2))
    if x2 > x1 and y2 > y1:
        roi = img[y1:y2, x1:x2]
        color_rect = np.full(roi.shape, bg_color, dtype=np.uint8)
        img[y1:y2, x1:x2] = cv2.addWeighted(color_rect, alpha, roi, 1.0 - alpha, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 2)


def run_dual_simulator(
    cam1_path=None,
    cam2_path=None,
    start1_sec=0.0,
    start2_sec=0.0,
    exercise="push_up",
    loop=True,
    enable_ws=True,
    save_output=None
):
    tracker = DualViewExerciseTracker(exercise_name=exercise)
    ws_server = None
    if enable_ws:
        ws_server = MockDualWebSocketServer()
        ws_server.start()

    # Otomatis deteksi file jika tidak dispesifikasikan
    if not cam1_path:
        default_pair = DEFAULT_EXERCISE_VIDEOS.get(exercise)
        if default_pair and Path(default_pair[0]).exists() and Path(default_pair[1]).exists():
            cam1_path, cam2_path = default_pair[0], default_pair[1]
            print(f"[Simulator] Otomatis memuat pasangan video latihan '{exercise}':")
            print(f"  - PV1 (Depan / Frontal)  : {cam1_path}")
            print(f"  - PV2 (Samping / Sagittal): {cam2_path}")
        else:
            print(f"[Error] Video default untuk latihan '{exercise}' tidak ditemukan di folder data/videos/!")
            return

    # Deteksi mana yang Frontal (PV1) dan mana yang Sagittal (PV2)
    c1_str = str(cam1_path).lower()
    c2_str = str(cam2_path).lower() if cam2_path else ""

    # Standarisasi:
    # front_path = POV Depan (PV1)
    # side_path  = POV Samping (PV2)
    if ("pv2" in c1_str or "side" in c1_str) and ("pv1" in c2_str or "front" in c2_str):
        front_path, side_path = cam2_path, cam1_path
        start_front, start_side = start2_sec, start1_sec
    else:
        front_path = cam1_path
        side_path = cam2_path if cam2_path and Path(cam2_path).exists() else cam1_path
        start_front, start_side = start1_sec, start2_sec

    cap_front = cv2.VideoCapture(str(front_path))
    cap_side = cv2.VideoCapture(str(side_path))

    if not cap_front.isOpened() or not cap_side.isOpened():
        print("[Error] Gagal membuka video Frontal atau Sagittal!")
        return

    # Ambil spesifikasi FPS
    fps_f = cap_front.get(cv2.CAP_PROP_FPS) or 30.0
    fps_s = cap_side.get(cv2.CAP_PROP_FPS) or 30.0
    target_fps = max(fps_f, fps_s)
    if target_fps <= 0 or np.isnan(target_fps) or target_fps > 120:
        target_fps = 30.0
    target_frame_time = 1.0 / target_fps

    # Inisialisasi posisi awal (Trimming / Offset)
    def apply_start_offsets(sf, ss):
        cap_front.set(cv2.CAP_PROP_POS_MSEC, max(0.0, sf * 1000.0))
        cap_side.set(cv2.CAP_PROP_POS_MSEC, max(0.0, ss * 1000.0))

    cur_start_front = max(0.0, float(start_front))
    cur_start_side = max(0.0, float(start_side))
    apply_start_offsets(cur_start_front, cur_start_side)

    # Inisialisasi model Pose untuk masing-masing kamera
    pose_front = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pose_side = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    writer = None
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    print("\n" + "="*70)
    print(" FITNESS TRACKING EYE - DUAL-VIEW MULTI-CAMERA FUSION ENGINE")
    print(f" Latihan: {exercise.upper()} | Target FPS: {target_fps:.1f}")
    print(f" Frontal (PV1): {front_path}")
    print(f" Sagittal (PV2): {side_path}")
    print(f" Offset Awal  : Frontal {cur_start_front:.2f}s | Sagittal {cur_start_side:.2f}s (Selisih: {cur_start_side - cur_start_front:+.2f}s)")
    print(" --------------------------------------------------------------------")
    print(" Kontrol Interaktif di Jendela Video:")
    print("   [  /  ]  : Geser offset Sagittal (PV2) mundur / maju (-/+ 0.1 detik)")
    print("   {  /  }  : Geser offset Sagittal (PV2) mundur / maju (-/+ 1.0 detik)")
    print("   SPASI    : Pause / Lanjutkan pemutaran")
    print("   R        : Reset kembali ke titik awal sinkronisasi")
    print("   Q        : Keluar dari simulator")
    print("="*70 + "\n")

    frame_count = 0
    fps_display = target_fps
    fps_timer = time.time()
    is_paused = False

    video_start_time = time.perf_counter()
    expected_frame_idx = 0

    while True:
        if is_paused:
            key = cv2.waitKey(50) & 0xFF
            if key == ord(' '):
                is_paused = False
                video_start_time = time.perf_counter() - (expected_frame_idx * target_frame_time)
            elif key == ord('q'):
                break
            continue

        # Wall-clock pacing
        elapsed_clock = time.perf_counter() - video_start_time
        target_frame_idx = int(elapsed_clock * target_fps)

        while expected_frame_idx < target_frame_idx - 1:
            ret_f = cap_front.grab()
            ret_s = cap_side.grab()
            if not ret_f or not ret_s:
                break
            expected_frame_idx += 1

        ret_f, frame_f = cap_front.read()
        ret_s, frame_s = cap_side.read()

        if not ret_f or not ret_s:
            if loop:
                apply_start_offsets(cur_start_front, cur_start_side)
                video_start_time = time.perf_counter()
                expected_frame_idx = 0
                continue
            else:
                break

        expected_frame_idx += 1
        frame_count += 1

        if frame_count % 15 == 0:
            now_t = time.time()
            fps_display = 15.0 / max(0.001, (now_t - fps_timer))
            fps_timer = now_t

        # Normalisasi ketinggian kedua frame:
        # Jika video portrait (1080x1920), norm_h = 680 agar lebar canvas seimbang (~760x680)
        hf, wf = frame_f.shape[:2]
        hs, ws = frame_s.shape[:2]
        norm_h = 680 if hf > wf else 540
        new_wf = int(wf * (norm_h / hf))
        new_ws = int(ws * (norm_h / hs))

        ff_resized = cv2.resize(frame_f, (new_wf, norm_h))
        fs_resized = cv2.resize(frame_s, (new_ws, norm_h))

        # Inferensi MediaPipe independen untuk Frontal & Sagittal
        rgbf = cv2.cvtColor(ff_resized, cv2.COLOR_BGR2RGB)
        rgbs = cv2.cvtColor(fs_resized, cv2.COLOR_BGR2RGB)
        rgbf.flags.writeable = False
        rgbs.flags.writeable = False

        res_f = pose_front.process(rgbf)
        res_s = pose_side.process(rgbs)

        lms_f = res_f.pose_landmarks.landmark if res_f.pose_landmarks else None
        lms_s = res_s.pose_landmarks.landmark if res_s.pose_landmarks else None

        # Evaluasi Biomekanik Multi-Kamera
        reps, stage, sag_angles, front_metrics, errors = tracker.process_dual_landmarks(lms_f, lms_s)
        is_form_valid = len(errors) == 0

        # Broadcast via WebSocket
        if ws_server:
            payload = {
                "type": "dual_pose_frame",
                "timestamp_ms": int(time.time() * 1000),
                "exercise": exercise,
                "reps": reps,
                "stage": stage,
                "is_valid_form": is_form_valid,
                "frontal_pv1": {
                    "detected": lms_f is not None,
                    "metrics": front_metrics
                },
                "sagittal_pv2": {
                    "detected": lms_s is not None,
                    "angles": sag_angles
                },
                "form_errors": errors,
                "sync_offset_sec": round(cur_start_side - cur_start_front, 3)
            }
            ws_server.broadcast(payload)

        # Gambar skeleton pada masing-masing frame
        line_color = (0, 255, 0) if is_form_valid else (0, 0, 255)
        if res_f.pose_landmarks:
            mp_drawing.draw_landmarks(
                ff_resized, res_f.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 140, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=line_color, thickness=2, circle_radius=2)
            )
        if res_s.pose_landmarks:
            mp_drawing.draw_landmarks(
                fs_resized, res_s.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 240, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=line_color, thickness=2, circle_radius=2)
            )

        # Gabungkan kedua frame secara Side-by-Side (Canvas Utama)
        canvas = np.hstack((ff_resized, fs_resized))
        canvas_h, canvas_w, _ = canvas.shape

        # Garis pemisah vertikal elegan di tengah
        cv2.line(canvas, (new_wf, 0), (new_wf, canvas_h), (0, 240, 255), 2)

        # =================================================================
        # HUD 1: KIRI ATAS - STATUS REPETISI UTAMA (Neon Glass Panel)
        # =================================================================
        reps_w = min(220, new_wf - 20)
        draw_glass_card(canvas, 10, 10, 10 + reps_w, 110, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.85)
        cv2.putText(canvas, f"EXERCISE: {exercise.upper()}", (18, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 240, 255), 1, cv2.LINE_AA)
        cv2.putText(canvas, f"REPS: {reps}", (18, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.15, (255, 255, 255), 2, cv2.LINE_AA)
        stage_color = (0, 255, 128) if stage == "UP" else (0, 165, 255)
        cv2.putText(canvas, f"STAGE: {stage} | {fps_display:.0f} FPS", (18, 96),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, stage_color, 2, cv2.LINE_AA)

        # =================================================================
        # HUD 2: TENGAH ATAS - SINKRONISASI OFFSET PILL
        # =================================================================
        pill_w = 160
        pill_x1 = max(10, new_wf - pill_w // 2)
        pill_x2 = min(canvas_w - 10, pill_x1 + pill_w)
        draw_glass_card(canvas, pill_x1, 10, pill_x2, 42, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.85)
        offset_text = f"Offset: {cur_start_side - cur_start_front:+.2f}s"
        cv2.putText(canvas, offset_text, (pill_x1 + 14, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1, cv2.LINE_AA)

        # =================================================================
        # HUD 3: KANAN ATAS - METRIK FUSI BIOMEKANIK (MULTI-SUDUT)
        # =================================================================
        all_metrics = []
        for k, v in sag_angles.items():
            all_metrics.append((f"Sagittal {k}", f"{v} deg"))
        for k, v in front_metrics.items():
            all_metrics.append((f"Frontal {k}", str(v)))

        if all_metrics:
            panel_w = min(240, new_ws - 20)
            panel_h = 32 + len(all_metrics) * 22
            rx1 = canvas_w - panel_w - 10
            ry1 = 10
            rx2 = canvas_w - 10
            ry2 = ry1 + panel_h

            draw_glass_card(canvas, rx1, ry1, rx2, ry2, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.85)
            cv2.putText(canvas, "BIOMECHANICS", (rx1 + 10, ry1 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 240, 255), 1, cv2.LINE_AA)

            for m_idx, (m_lbl, m_val) in enumerate(all_metrics):
                my = ry1 + 40 + (m_idx * 21)
                cv2.putText(canvas, f"{m_lbl}: {m_val}", (rx1 + 10, my),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)

        # =================================================================
        # HUD 4: BOTTOM BANNERS (LABEL KAMERA)
        # =================================================================
        draw_glass_card(canvas, 10, canvas_h - 40, new_wf - 10, canvas_h - 10, bg_color=(15, 20, 35), border_color=(255, 140, 0), alpha=0.8)
        cv2.putText(canvas, "CAM 1: DEPAN (PV1 / FRONTAL)", (20, canvas_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 160, 50), 1, cv2.LINE_AA)

        draw_glass_card(canvas, new_wf + 10, canvas_h - 40, canvas_w - 10, canvas_h - 10, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.8)
        cv2.putText(canvas, "CAM 2: SAMPING (PV2 / SAGITTAL)", (new_wf + 20, canvas_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 240, 255), 1, cv2.LINE_AA)

        # =================================================================
        # HUD 5: ALERT BANNER JIKA ADA KESALAHAN FORM
        # =================================================================
        if errors:
            for e_idx, err_msg in enumerate(errors):
                ey = canvas_h - 75 - (e_idx * 30)
                draw_glass_card(canvas, canvas_w // 2 - 170, ey, canvas_w // 2 + 170, ey + 26,
                                bg_color=(0, 0, 160), border_color=(0, 0, 255), alpha=0.9)
                cv2.putText(canvas, f"! {err_msg}", (canvas_w // 2 - 160, ey + 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1, cv2.LINE_AA)

        # Tampilkan canvas terpadu
        cv2.imshow("Fitness Tracking Eye - Dual-View Multi-Camera Simulator", canvas)

        if writer:
            writer.write(canvas)
        elif save_output and not writer:
            writer = cv2.VideoWriter(save_output, fourcc, target_fps, (canvas_w, canvas_h))
            writer.write(canvas)

        # Kontrol Keyboard Interaktif
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            is_paused = True
        elif key == ord('r'):
            # Reset
            apply_start_offsets(cur_start_front, cur_start_side)
            video_start_time = time.perf_counter()
            expected_frame_idx = 0
            tracker.counter = 0
            print(f"[Sync] Reset posisi video ke awal (Offset: {cur_start_side - cur_start_front:+.2f}s)")
        elif key == ord(']'):
            cur_start_side += 0.1
            apply_start_offsets(cur_start_front, cur_start_side)
            print(f"[Sync] Sagittal (PV2) maju +0.1s -> Selisih baru: {cur_start_side - cur_start_front:+.2f}s")
        elif key == ord('['):
            cur_start_side = max(0.0, cur_start_side - 0.1)
            apply_start_offsets(cur_start_front, cur_start_side)
            print(f"[Sync] Sagittal (PV2) mundur -0.1s -> Selisih baru: {cur_start_side - cur_start_front:+.2f}s")
        elif key == ord('}'):
            cur_start_side += 1.0
            apply_start_offsets(cur_start_front, cur_start_side)
            print(f"[Sync] Sagittal (PV2) maju +1.0s -> Selisih baru: {cur_start_side - cur_start_front:+.2f}s")
        elif key == ord('{'):
            cur_start_side = max(0.0, cur_start_side - 1.0)
            apply_start_offsets(cur_start_front, cur_start_side)
            print(f"[Sync] Sagittal (PV2) mundur -1.0s -> Selisih baru: {cur_start_side - cur_start_front:+.2f}s")

    cap_front.release()
    cap_side.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("[Simulator] Sesi Dual-View selesai.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fitness Tracking Eye - Dual-View Fusion Simulator")
    parser.add_argument("--cam1", type=str, default=None, help="Path ke video Kamera 1 (PV1 / Frontal)")
    parser.add_argument("--cam2", type=str, default=None, help="Path ke video Kamera 2 (PV2 / Sagittal)")
    parser.add_argument("--start1", type=float, default=0.0, help="Titik mulai video Cam 1 dalam detik")
    parser.add_argument("--start2", type=float, default=0.0, help="Titik mulai video Cam 2 dalam detik")
    parser.add_argument("--exercise", type=str, default="push_up",
                        choices=["push_up", "squat_jump", "pull_up", "sit_up", "vertical_jump"],
                        help="Jenis latihan yang dievaluasi")
    parser.add_argument("--no-loop", action="store_true", help="Jangan ulang video otomatis")
    parser.add_argument("--no-ws", action="store_true", help="Nonaktifkan streaming WebSocket")
    parser.add_argument("--save-output", type=str, default=None, help="Path simpan video hasil fusi .mp4")

    args = parser.parse_args()
    run_dual_simulator(
        cam1_path=args.cam1,
        cam2_path=args.cam2,
        start1_sec=args.start1,
        start2_sec=args.start2,
        exercise=args.exercise,
        loop=not args.no_loop,
        enable_ws=not args.no_ws,
        save_output=args.save_output
    )
