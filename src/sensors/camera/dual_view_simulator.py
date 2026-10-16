"""
Fitness Tracking Eye - Dual-View Video Simulator & Multi-Camera Fusion Engine
=============================================================================
Skrip simulator sinkronisasi dua sudut pandang (Dual-View / Multi-Camera):
1. Membaca dua sumber video (Kamera 1: Samping/Sagittal, Kamera 2: Depan/Frontal).
2. Menyelaraskan garis waktu (temporal sync) via offset timestamp (--start1 & --start2).
3. Pacing real-time 1.0x terkunci ke jam dinding (wall-clock) dengan kompensasi AI delay.
4. Menjalankan estimasi pose 3D independen untuk kedua kamera via MediaPipe BlazePose.
5. Fusi Biomekanik Multi-Sudut (Sagittal: Sudut Siku & Kelurusan Tulang Punggung;
   Frontal: Keseimbangan Kemiringan Bahu & Lebar Bukaan Telapak Tangan).
6. Tampilan antarmuka visual terpadu Side-by-Side dengan Glassmorphism HUD.
7. Kontrol sinkronisasi live interaktif: '[' / ']' untuk geser offset 0.1s saat video berjalan.
8. Siaran data skeleton terpadu via WebSocket (ws://localhost:8765).
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


class DualViewExerciseTracker:
    """Mesin evaluasi fusi biomekanik multi-sudut (Sagittal + Frontal)."""
    def __init__(self, config_path="config/exercise_config.yaml", exercise_name="push_up"):
        self.exercise_name = exercise_name
        self.counter = 0
        self.stage = "UP"  # "UP" or "DOWN"
        self.last_transition_time = time.time()
        self.min_transition_sec = 0.35  # Anti-jitter debounce
        self.form_errors = []
        self.cam1_angles = {}
        self.cam2_metrics = {}
        self.config = self._load_config(config_path)

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

    def process_dual_landmarks(self, lms1, lms2):
        """
        Fusi metrik biomekanik:
        - lms1 (Cam 1 / Sagittal View): Sudut sendi fleksi-ekstensi & evaluasi repetisi
        - lms2 (Cam 2 / Frontal View): Keseimbangan simetri bahu & bukaan tangan
        """
        self.form_errors = []
        self.cam1_angles = {}
        self.cam2_metrics = {}
        now = time.time()

        # =================================================================
        # 1. EVALUASI KAMERA 1 (SAGITTAL / SAMPING)
        # =================================================================
        if lms1 is not None:
            # Auto-detect profil tubuh (Kiri vs Kanan)
            l_vis = (lms1[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility +
                     lms1[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility +
                     lms1[mp_pose.PoseLandmark.LEFT_HIP.value].visibility) / 3.0
            r_vis = (lms1[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility +
                     lms1[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility +
                     lms1[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility) / 3.0
            use_left = l_vis >= r_vis

            sh1 = [lms1[11 if use_left else 12].x, lms1[11 if use_left else 12].y]
            el1 = [lms1[13 if use_left else 14].x, lms1[13 if use_left else 14].y]
            wr1 = [lms1[15 if use_left else 16].x, lms1[15 if use_left else 16].y]
            hp1 = [lms1[23 if use_left else 24].x, lms1[23 if use_left else 24].y]
            kn1 = [lms1[25 if use_left else 26].x, lms1[25 if use_left else 26].y]
            ak1 = [lms1[27 if use_left else 28].x, lms1[27 if use_left else 28].y]

            if self.exercise_name == "push_up":
                elbow_angle = self.calculate_angle(sh1, el1, wr1)
                body_angle = self.calculate_angle(sh1, hp1, ak1)
                self.cam1_angles["Elbow Angle"] = round(elbow_angle, 1)
                self.cam1_angles["Body Line"] = round(body_angle, 1)

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

            elif "squat" in self.exercise_name:
                knee_angle = self.calculate_angle(hp1, kn1, ak1)
                self.cam1_angles["Knee Angle"] = round(knee_angle, 1)

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

                if kn1[0] > ak1[0] + 0.06:
                    self.form_errors.append("Lutut Lewati Jari Kaki")

            elif self.exercise_name == "sit_up":
                hip_angle = self.calculate_angle(sh1, hp1, kn1)
                self.cam1_angles["Hip Angle"] = round(hip_angle, 1)

                if hip_angle > 130 and self.stage != "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "DOWN"
                        self.last_transition_time = now
                elif hip_angle < 75 and self.stage == "DOWN":
                    if now - self.last_transition_time > self.min_transition_sec:
                        self.stage = "UP"
                        self.counter += 1
                        self.last_transition_time = now

        # =================================================================
        # 2. EVALUASI KAMERA 2 (FRONTAL / DEPAN)
        # =================================================================
        if lms2 is not None:
            l_sh = [lms2[11].x, lms2[11].y]
            r_sh = [lms2[12].x, lms2[12].y]
            l_wr = [lms2[15].x, lms2[15].y]
            r_wr = [lms2[16].x, lms2[16].y]
            l_kn = [lms2[25].x, lms2[25].y]
            r_kn = [lms2[26].x, lms2[26].y]
            l_ak = [lms2[27].x, lms2[27].y]
            r_ak = [lms2[28].x, lms2[28].y]

            # Kemiringan Bahu (Shoulder Tilt)
            dx = abs(r_sh[0] - l_sh[0])
            dy = r_sh[1] - l_sh[1]
            shoulder_tilt_deg = abs(np.arctan2(dy, max(0.001, dx)) * 180.0 / np.pi)
            self.cam2_metrics["Shoulder Tilt"] = f"{round(shoulder_tilt_deg, 1)} deg"

            if shoulder_tilt_deg > 6.5:
                self.form_errors.append("Bahu Miring / Asimetris (Frontal)")

            # Rasio Bukaan Tangan vs Bahu (Hand Stance Width)
            sh_dist = np.hypot(r_sh[0] - l_sh[0], r_sh[1] - l_sh[1])
            wr_dist = np.hypot(r_wr[0] - l_wr[0], r_wr[1] - l_wr[1])
            if sh_dist > 0.05:
                width_ratio = wr_dist / sh_dist
                self.cam2_metrics["Hand Width"] = f"{round(width_ratio, 2)}x Bahu"
                if width_ratio > 2.3:
                    self.form_errors.append("Posisi Tangan Terlalu Lebar")
                elif width_ratio < 0.75:
                    self.form_errors.append("Posisi Tangan Terlalu Sempit")

            # Cek Lutut Masuk ke Dalam (Valgus) untuk Squat
            if "squat" in self.exercise_name:
                knee_dist = np.hypot(r_kn[0] - l_kn[0], r_kn[1] - l_kn[1])
                ankle_dist = np.hypot(r_ak[0] - l_ak[0], r_ak[1] - l_ak[1])
                if ankle_dist > 0.05:
                    if knee_dist < ankle_dist * 0.70:
                        self.form_errors.append("Lutut Tertekuk Ke Dalam (Valgus)")

        return self.counter, self.stage, self.cam1_angles, self.cam2_metrics, self.form_errors


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
    """Menggambar panel HUD semi-transparan via ROI slicing cepat."""
    h_img, w_img, _ = img.shape
    x1, y1 = max(0, int(x1)), max(0, int(y1))
    x2, y2 = min(w_img, int(x2)), min(h_img, int(y2))
    if x2 > x1 and y2 > y1:
        roi = img[y1:y2, x1:x2]
        color_rect = np.full(roi.shape, bg_color, dtype=np.uint8)
        img[y1:y2, x1:x2] = cv2.addWeighted(color_rect, alpha, roi, 1.0 - alpha, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 2)


def run_dual_simulator(
    cam1_path,
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

    # Buka Kamera 1
    if not cam1_path or not Path(cam1_path).exists():
        print(f"[Error] File video Kamera 1 tidak ditemukan: {cam1_path}")
        return
    cap1 = cv2.VideoCapture(str(cam1_path))

    # Buka Kamera 2 (jika tidak disediakan, gunakan kamera 1 sebagai simulasi cermin/demo)
    using_demo_cam2 = False
    if cam2_path and Path(cam2_path).exists():
        cap2 = cv2.VideoCapture(str(cam2_path))
    else:
        print("[Simulator] Video Kamera 2 tidak dispesifikasikan. Menjalankan mode DEMO dengan klon Kamera 1.")
        cap2 = cv2.VideoCapture(str(cam1_path))
        using_demo_cam2 = True

    if not cap1.isOpened() or not cap2.isOpened():
        print("[Error] Gagal membuka stream video Kamera 1 atau Kamera 2!")
        return

    # Ambil spesifikasi FPS
    fps1 = cap1.get(cv2.CAP_PROP_FPS) or 30.0
    fps2 = cap2.get(cv2.CAP_PROP_FPS) or 30.0
    target_fps = max(fps1, fps2)
    if target_fps <= 0 or np.isnan(target_fps) or target_fps > 120:
        target_fps = 30.0
    target_frame_time = 1.0 / target_fps

    # Inisialisasi posisi awal (Trimming / Offset)
    def apply_start_offsets(s1, s2):
        cap1.set(cv2.CAP_PROP_POS_MSEC, max(0.0, s1 * 1000.0))
        cap2.set(cv2.CAP_PROP_POS_MSEC, max(0.0, s2 * 1000.0))

    cur_start1 = max(0.0, float(start1_sec))
    cur_start2 = max(0.0, float(start2_sec))
    apply_start_offsets(cur_start1, cur_start2)

    # Inisialisasi model Pose untuk masing-masing kamera
    pose1 = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    pose2 = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Output canvas size: Normalized height 540
    norm_h = 540
    writer = None
    if save_output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # Lebar canvas total dihitung nanti setelah frame pertama terbaca
        print(f"[Simulator] Hasil video fusi akan disimpan ke: {save_output}")

    print("\n" + "="*70)
    print(" FITNESS TRACKING EYE - DUAL-VIEW FUSION ENGINE SIMULATOR")
    print(f" Latihan: {exercise.upper()} | Target FPS: {target_fps:.1f}")
    print(f" Offset Awal -> Cam1: {cur_start1:.2f}s | Cam2: {cur_start2:.2f}s (Selisih: {cur_start2 - cur_start1:+.2f}s)")
    print(" --------------------------------------------------------------------")
    print(" Kontrol Interaktif di Jendela Video:")
    print("   [  /  ]  : Geser offset Cam 2 mundur / maju (-/+ 0.1 detik)")
    print("   {  /  }  : Geser offset Cam 2 mundur / maju (-/+ 1.0 detik)")
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
            ret1 = cap1.grab()
            ret2 = cap2.grab()
            if not ret1 or not ret2:
                break
            expected_frame_idx += 1

        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            if loop:
                apply_start_offsets(cur_start1, cur_start2)
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

        # Normalisasi ketinggian kedua frame agar presisi sejajar
        h1, w1 = frame1.shape[:2]
        h2, w2 = frame2.shape[:2]
        new_w1 = int(w1 * (norm_h / h1))
        new_w2 = int(w2 * (norm_h / h2))

        f1_resized = cv2.resize(frame1, (new_w1, norm_h))
        f2_resized = cv2.resize(frame2, (new_w2, norm_h))

        # Inferensi MediaPipe untuk Cam 1 & Cam 2
        rgb1 = cv2.cvtColor(f1_resized, cv2.COLOR_BGR2RGB)
        rgb2 = cv2.cvtColor(f2_resized, cv2.COLOR_BGR2RGB)
        rgb1.flags.writeable = False
        rgb2.flags.writeable = False

        res1 = pose1.process(rgb1)
        res2 = pose2.process(rgb2)

        lms1 = res1.pose_landmarks.landmark if res1.pose_landmarks else None
        lms2 = res2.pose_landmarks.landmark if res2.pose_landmarks else None

        # Evaluasi Biomekanik Multi-Kamera
        reps, stage, cam1_angles, cam2_metrics, errors = tracker.process_dual_landmarks(lms1, lms2)
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
                "cam1_sagittal": {
                    "detected": lms1 is not None,
                    "angles": cam1_angles
                },
                "cam2_frontal": {
                    "detected": lms2 is not None,
                    "metrics": cam2_metrics
                },
                "form_errors": errors,
                "sync_offset_sec": round(cur_start2 - cur_start1, 3)
            }
            ws_server.broadcast(payload)

        # Gambar skeleton pada masing-masing frame
        line_color = (0, 255, 0) if is_form_valid else (0, 0, 255)
        if res1.pose_landmarks:
            mp_drawing.draw_landmarks(
                f1_resized, res1.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 240, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=line_color, thickness=2, circle_radius=2)
            )
        if res2.pose_landmarks:
            mp_drawing.draw_landmarks(
                f2_resized, res2.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(255, 120, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=line_color, thickness=2, circle_radius=2)
            )

        # Gabungkan kedua frame secara Side-by-Side (Canvas Utama)
        canvas = np.hstack((f1_resized, f2_resized))
        canvas_h, canvas_w, _ = canvas.shape

        # Garis pemisah vertikal elegan di tengah
        cv2.line(canvas, (new_w1, 0), (new_w1, canvas_h), (0, 240, 255), 2)

        # =================================================================
        # HUD 1: KIRI ATAS - STATUS REPETISI UTAMA (Neon Glass Panel)
        # =================================================================
        draw_glass_card(canvas, 15, 15, 275, 120, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.8)
        cv2.putText(canvas, f"EXERCISE: {exercise.upper()}", (25, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (0, 240, 255), 1, cv2.LINE_AA)
        cv2.putText(canvas, f"REPS: {reps}", (25, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.15, (255, 255, 255), 2, cv2.LINE_AA)
        stage_color = (0, 255, 128) if stage == "UP" else (0, 165, 255)
        cv2.putText(canvas, f"STAGE: {stage}  |  {fps_display:.0f} FPS", (25, 106),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, stage_color, 2, cv2.LINE_AA)

        # =================================================================
        # HUD 2: TENGAH ATAS - LABEL KAMERA & STATUS SINKRONISASI
        # =================================================================
        draw_glass_card(canvas, new_w1 - 180, 15, new_w1 + 180, 65, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.85)
        cv2.putText(canvas, "DUAL-VIEW FUSION", (new_w1 - 85, 36),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 240, 255), 1, cv2.LINE_AA)
        offset_text = f"Offset Cam2: {cur_start2 - cur_start1:+.2f}s"
        cv2.putText(canvas, offset_text, (new_w1 - 80, 56),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (200, 200, 200), 1, cv2.LINE_AA)

        # Label Nama Masing-Masing Kamera
        cv2.putText(canvas, "CAM 1: SAGITTAL (SIDE VIEW)", (25, canvas_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 240, 255), 1, cv2.LINE_AA)
        cv2.putText(canvas, "CAM 2: FRONTAL (FRONT VIEW)" if not using_demo_cam2 else "CAM 2: DEMO (MIRROR/FRONT)",
                    (new_w1 + 25, canvas_h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 140, 0), 1, cv2.LINE_AA)

        # =================================================================
        # HUD 3: KANAN ATAS - METRIK FUSI BIOMEKANIK (MULTI-SUDUT)
        # =================================================================
        all_metrics = []
        for k, v in cam1_angles.items():
            all_metrics.append((f"Cam1 {k}", f"{v} deg"))
        for k, v in cam2_metrics.items():
            all_metrics.append((f"Cam2 {k}", str(v)))

        if all_metrics:
            panel_w = 280
            panel_h = 35 + len(all_metrics) * 24
            rx1 = canvas_w - panel_w - 15
            ry1 = 15
            rx2 = canvas_w - 15
            ry2 = ry1 + panel_h

            draw_glass_card(canvas, rx1, ry1, rx2, ry2, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.8)
            cv2.putText(canvas, "FUSED BIOMECHANICS", (rx1 + 14, ry1 + 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 240, 255), 1, cv2.LINE_AA)

            for m_idx, (m_lbl, m_val) in enumerate(all_metrics):
                my = ry1 + 45 + (m_idx * 23)
                cv2.putText(canvas, f"{m_lbl}: {m_val}", (rx1 + 14, my),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

            # Warning banner jika ada kesalahan form
            if errors:
                for e_idx, err_msg in enumerate(errors):
                    ey = ry2 + 10 + (e_idx * 30)
                    draw_glass_card(canvas, canvas_w - 320, ey, canvas_w - 15, ey + 26,
                                    bg_color=(0, 0, 160), border_color=(0, 0, 255), alpha=0.9)
                    cv2.putText(canvas, f"! {err_msg}", (canvas_w - 310, ey + 18),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1, cv2.LINE_AA)

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
            apply_start_offsets(cur_start1, cur_start2)
            video_start_time = time.perf_counter()
            expected_frame_idx = 0
            tracker.counter = 0
            print(f"[Sync] Reset posisi video ke awal (Offset: {cur_start2 - cur_start1:+.2f}s)")
        elif key == ord(']'):
            cur_start2 += 0.1
            apply_start_offsets(cur_start1, cur_start2)
            print(f"[Sync] Cam 2 maju +0.1s -> Selisih baru: {cur_start2 - cur_start1:+.2f}s")
        elif key == ord('['):
            cur_start2 = max(0.0, cur_start2 - 0.1)
            apply_start_offsets(cur_start1, cur_start2)
            print(f"[Sync] Cam 2 mundur -0.1s -> Selisih baru: {cur_start2 - cur_start1:+.2f}s")
        elif key == ord('}'):
            cur_start2 += 1.0
            apply_start_offsets(cur_start1, cur_start2)
            print(f"[Sync] Cam 2 maju +1.0s -> Selisih baru: {cur_start2 - cur_start1:+.2f}s")
        elif key == ord('{'):
            cur_start2 = max(0.0, cur_start2 - 1.0)
            apply_start_offsets(cur_start1, cur_start2)
            print(f"[Sync] Cam 2 mundur -1.0s -> Selisih baru: {cur_start2 - cur_start1:+.2f}s")

    cap1.release()
    cap2.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("[Simulator] Sesi Dual-View selesai.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fitness Tracking Eye - Dual-View Fusion Simulator")
    parser.add_argument("--cam1", type=str, required=True, help="Path ke berkas video Kamera 1 (Sagittal/Side View)")
    parser.add_argument("--cam2", type=str, default=None, help="Path ke berkas video Kamera 2 (Frontal/Front View)")
    parser.add_argument("--start1", type=float, default=0.0, help="Titik mulai video Cam 1 dalam detik (cth: 3.5)")
    parser.add_argument("--start2", type=float, default=0.0, help="Titik mulai video Cam 2 dalam detik (cth: 8.2)")
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
