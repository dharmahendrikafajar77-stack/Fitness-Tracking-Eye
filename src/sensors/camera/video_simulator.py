"""
Fitness Tracking Eye - Video Simulator & Mock Camera Node
=========================================================
Skrip simulator untuk memproses video rekaman latihan (.mp4) atau webcam lokal:
1. Membaca video latihan secara frame-by-frame pada kecepatan 1.0x asli (real-time pacing).
2. Mengekstrak 33 3D keypoints pose menggunakan MediaPipe BlazePose.
3. Menghitung sudut sendi biomekanik & repetisi berdasarkan config/exercise_config.yaml.
4. Menyiarkan teks koordinat JSON skeleton secara real-time via WebSocket (port 8765).
5. Menampilkan antarmuka visual HUD profesional tanpa teks bertumpuk.
6. (Opsional) Menyimpan rekaman hasil overlay untuk review pasca-latihan.
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


class ExerciseStateTracker:
    def __init__(self, config_path="config/exercise_config.yaml", exercise_name="push_up"):
        self.exercise_name = exercise_name
        self.counter = 0
        self.stage = "UP"  # "UP" or "DOWN"
        self.last_transition_time = time.time()
        self.min_transition_sec = 0.35  # Anti-bounce / debouncing filter
        self.form_errors = []
        self.current_angles = {}
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

    def process_landmarks(self, landmarks, frame_w, frame_h):
        """Mengevaluasi pose berdasarkan jenis latihan dan threshold di config."""
        self.form_errors = []
        self.current_angles = {}
        now = time.time()
        
        # Deteksi sisi tubuh paling dominan (Kiri vs Kanan)
        l_vis = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].visibility +
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility +
                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].visibility) / 3.0
        r_vis = (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].visibility +
                 landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].visibility +
                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].visibility) / 3.0
        use_left = l_vis >= r_vis

        sh_idx = mp_pose.PoseLandmark.LEFT_SHOULDER.value if use_left else mp_pose.PoseLandmark.RIGHT_SHOULDER.value
        el_idx = mp_pose.PoseLandmark.LEFT_ELBOW.value if use_left else mp_pose.PoseLandmark.RIGHT_ELBOW.value
        wr_idx = mp_pose.PoseLandmark.LEFT_WRIST.value if use_left else mp_pose.PoseLandmark.RIGHT_WRIST.value
        hp_idx = mp_pose.PoseLandmark.LEFT_HIP.value if use_left else mp_pose.PoseLandmark.RIGHT_HIP.value
        kn_idx = mp_pose.PoseLandmark.LEFT_KNEE.value if use_left else mp_pose.PoseLandmark.RIGHT_KNEE.value
        ak_idx = mp_pose.PoseLandmark.LEFT_ANKLE.value if use_left else mp_pose.PoseLandmark.RIGHT_ANKLE.value

        # Ekstrak titik-titik sendi utama
        def get_pt(idx):
            lm = landmarks[idx]
            return [lm.x, lm.y]

        # ==========================================
        # 1. PUSH UP
        # ==========================================
        if self.exercise_name == "push_up":
            shoulder = get_pt(sh_idx)
            elbow = get_pt(el_idx)
            wrist = get_pt(wr_idx)
            hip = get_pt(hp_idx)
            ankle = get_pt(ak_idx)

            elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
            body_angle = self.calculate_angle(shoulder, hip, ankle)
            
            self.current_angles["Elbow Angle"] = round(elbow_angle, 1)
            self.current_angles["Body Line"] = round(body_angle, 1)

            cfg = self.config.get("push_up", {})
            up_th = cfg.get("elbow_angle", {}).get("up_threshold", 155)
            down_th = cfg.get("elbow_angle", {}).get("down_threshold", 95)

            # State Machine Push Up:
            # Siku turun < 95 deg -> Masuk status DOWN
            if elbow_angle < down_th and self.stage != "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "DOWN"
                    self.last_transition_time = now

            # Siku naik kembali > 155 deg dari posisi DOWN -> Selesaikan 1 Repetisi!
            elif elbow_angle > up_th and self.stage == "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "UP"
                    self.counter += 1
                    self.last_transition_time = now

            # Form check: Punggung melengkung (hip sag)
            if body_angle < 150:
                self.form_errors.append("Punggung Melengkung")

        # ==========================================
        # 2. SQUAT / SQUAT JUMP
        # ==========================================
        elif "squat" in self.exercise_name:
            hip = get_pt(hp_idx)
            knee = get_pt(kn_idx)
            ankle = get_pt(ak_idx)
            
            knee_angle = self.calculate_angle(hip, knee, ankle)
            self.current_angles["Knee Angle"] = round(knee_angle, 1)

            cfg = self.config.get("squat_jump", {})
            stand_th = cfg.get("knee_angle", {}).get("stand_threshold", 160)
            squat_th = cfg.get("knee_angle", {}).get("squat_threshold", 95)

            # Jongkok < 95 deg -> DOWN
            if knee_angle < squat_th and self.stage != "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "DOWN"
                    self.last_transition_time = now

            # Berdiri kembali > 160 deg -> Repetisi Sah!
            elif knee_angle > stand_th and self.stage == "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "UP"
                    self.counter += 1
                    self.last_transition_time = now

            # Form check: lutut melewati ujung jari kaki
            if knee[0] > ankle[0] + 0.06:
                self.form_errors.append("Lutut Terlalu Maju")

        # ==========================================
        # 3. SIT UP
        # ==========================================
        elif self.exercise_name == "sit_up":
            shoulder = get_pt(sh_idx)
            hip = get_pt(hp_idx)
            knee = get_pt(kn_idx)

            hip_angle = self.calculate_angle(shoulder, hip, knee)
            self.current_angles["Hip Angle"] = round(hip_angle, 1)

            cfg = self.config.get("sit_up", {})
            down_th = cfg.get("hip_angle", {}).get("down_threshold", 130)
            up_th = cfg.get("hip_angle", {}).get("up_threshold", 75)

            if hip_angle > down_th and self.stage != "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "DOWN"
                    self.last_transition_time = now
            elif hip_angle < up_th and self.stage == "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "UP"
                    self.counter += 1
                    self.last_transition_time = now

        # ==========================================
        # 4. PULL UP
        # ==========================================
        elif self.exercise_name == "pull_up":
            shoulder = get_pt(sh_idx)
            elbow = get_pt(el_idx)
            wrist = get_pt(wr_idx)

            elbow_angle = self.calculate_angle(shoulder, elbow, wrist)
            self.current_angles["Elbow Angle"] = round(elbow_angle, 1)

            cfg = self.config.get("pull_up", {})
            hang_th = cfg.get("elbow_angle", {}).get("hang_threshold", 150)
            up_th = cfg.get("elbow_angle", {}).get("up_threshold", 75)

            if elbow_angle > hang_th and self.stage != "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "DOWN"
                    self.last_transition_time = now
            elif elbow_angle < up_th and self.stage == "DOWN":
                if now - self.last_transition_time > self.min_transition_sec:
                    self.stage = "UP"
                    self.counter += 1
                    self.last_transition_time = now

        # Fallback
        else:
            hip = get_pt(hp_idx)
            knee = get_pt(kn_idx)
            ankle = get_pt(ak_idx)
            self.current_angles["Joint Angle"] = round(self.calculate_angle(hip, knee, ankle), 1)

        return self.counter, self.stage, self.current_angles, self.form_errors


class MockWebSocketServer:
    """Server WebSocket mandiri untuk memancarkan teks JSON skeleton ke Web/Mobile App."""
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
            print(f"[WebSocket] Mock Server aktif di ws://{self.host}:{self.port}")
        except ImportError:
            print("[WebSocket] Pustaka 'websockets' belum terpasang. Mode broadcast dinonaktifkan.")

    def _run_server(self):
        import websockets
        async def handler(websocket):
            self.connected_clients.add(websocket)
            print(f"[WebSocket] Klien terhubung! Total klien: {len(self.connected_clients)}")
            try:
                await websocket.wait_closed()
            finally:
                self.connected_clients.remove(websocket)
                print(f"[WebSocket] Klien terputus. Sisa klien: {len(self.connected_clients)}")

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
    """Menggambar panel HUD semi-transparan (glassmorphism) via ROI slicing cepat tanpa copy full image."""
    h_img, w_img, _ = img.shape
    x1, y1 = max(0, int(x1)), max(0, int(y1))
    x2, y2 = min(w_img, int(x2)), min(h_img, int(y2))
    if x2 > x1 and y2 > y1:
        roi = img[y1:y2, x1:x2]
        color_rect = np.full(roi.shape, bg_color, dtype=np.uint8)
        img[y1:y2, x1:x2] = cv2.addWeighted(color_rect, alpha, roi, 1.0 - alpha, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), border_color, 2)


def run_simulator(video_path=None, exercise="push_up", loop=True, enable_ws=True, save_output=None):
    tracker = ExerciseStateTracker(exercise_name=exercise)
    ws_server = None
    if enable_ws:
        ws_server = MockWebSocketServer()
        ws_server.start()

    # Inisialisasi video input
    if video_path and Path(video_path).exists():
        print(f"[Simulator] Membaca video simulasi dari: {video_path}")
        cap = cv2.VideoCapture(str(video_path))
    else:
        print("[Simulator] Tidak ada file video valid yang diberikan. Membuka WEBCAM lokal default...")
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[Error] Tidak dapat membuka sumber video!")
        return

    # Ambil FPS asli video
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    if video_fps <= 0 or np.isnan(video_fps) or video_fps > 120:
        video_fps = 30.0
    target_frame_time = 1.0 / video_fps

    # Video Writer jika menyimpan review video
    writer = None
    if save_output:
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(save_output, fourcc, video_fps, (w, h))
        print(f"[Simulator] Menyimpan rekaman review video ke: {save_output}")

    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    print(f"\n" + "="*60)
    print(f" FITNESS TRACKING EYE - SIMULATOR AKTIF")
    print(f" Latihan: {exercise.upper()} | Target FPS: {video_fps:.1f} (Real-Time Pacing)")
    print(f" Tekan 'q' di jendela video untuk berhenti.")
    print("="*60 + "\n")

    frame_count = 0
    fps_display = video_fps
    fps_timer = time.time()

    # Wall-clock real-time synchronization tracker
    video_start_time = time.perf_counter()
    expected_frame_idx = 0

    while True:
        # Pacing: Cek apakah pemrosesan tertinggal dari wall-clock real-time
        if video_path:
            elapsed_clock = time.perf_counter() - video_start_time
            target_frame_idx = int(elapsed_clock * video_fps)

            # Jika komputasi AI sempat tertinggal > 1 frame, skip frame untuk menyusul seketika
            while expected_frame_idx < target_frame_idx - 1:
                ret = cap.grab()
                if not ret:
                    break
                expected_frame_idx += 1

        ret, frame = cap.read()
        if not ret:
            if loop and video_path:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                video_start_time = time.perf_counter()
                expected_frame_idx = 0
                continue
            else:
                break

        expected_frame_idx += 1
        frame_count += 1
        h, w, _ = frame.shape
        
        # Hitung real-time FPS display setiap 15 frame
        if frame_count % 15 == 0:
            now_t = time.time()
            fps_display = 15.0 / max(0.001, (now_t - fps_timer))
            fps_timer = now_t

        # Konversi BGR -> RGB untuk MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = pose.process(rgb_frame)
        rgb_frame.flags.writeable = True

        landmarks_json = []
        is_valid_form = True

        if results.pose_landmarks:
            lms = results.pose_landmarks.landmark
            reps, stage, angles, errors = tracker.process_landmarks(lms, w, h)
            is_valid_form = len(errors) == 0

            # Siapkan data JSON untuk broadcast WebSocket
            for i, lm in enumerate(lms):
                landmarks_json.append({
                    "id": i,
                    "x": round(lm.x, 4),
                    "y": round(lm.y, 4),
                    "z": round(lm.z, 4),
                    "vis": round(lm.visibility, 3)
                })

            # Broadcast ke WebSocket
            if ws_server:
                payload = {
                    "type": "pose_frame",
                    "camera_id": "cam_01_simulated",
                    "timestamp_ms": int(time.time() * 1000),
                    "exercise": exercise,
                    "reps": reps,
                    "stage": stage,
                    "angles": angles,
                    "form_errors": errors,
                    "landmarks": landmarks_json
                }
                ws_server.broadcast(payload)

            # Warna Garis Skeleton: Hijau (Form Benar) vs Merah (Form Salah)
            line_color = (0, 255, 0) if is_valid_form else (0, 0, 255)
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 240, 255), thickness=2, circle_radius=3),
                mp_drawing.DrawingSpec(color=line_color, thickness=3, circle_radius=2)
            )

            # =========================================================
            # HUD KANAN ATAS: KARTU BIOMEKANIK (TANPA TEKS BERTUMPUK!)
            # =========================================================
            card_w = 270
            card_h = 36 + len(angles) * 28
            rx1 = w - card_w - 15
            ry1 = 15
            rx2 = w - 15
            ry2 = ry1 + card_h

            # Background Card semi-transparan (Dark Navy)
            draw_glass_card(frame, rx1, ry1, rx2, ry2, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.75)

            # Judul Kartu Biomekanik
            cv2.putText(frame, "BIOMECHANICS", (rx1 + 14, ry1 + 22),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 240, 255), 1, cv2.LINE_AA)

            # Tiap sudut sendi ditulis di barisnya masing-masing secara terpisah
            for line_idx, (angle_name, angle_val) in enumerate(angles.items()):
                text_y = ry1 + 48 + (line_idx * 26)
                cv2.putText(frame, f"{angle_name}: {angle_val} deg", (rx1 + 14, text_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

            # =========================================================
            # KARTU PERINGATAN (WARNING BANNER) JIKA ADA KESALAHAN FORM
            # =========================================================
            if errors:
                warn_y1 = ry2 + 10
                for err_idx, err_msg in enumerate(errors):
                    wy = warn_y1 + (err_idx * 34)
                    draw_glass_card(frame, w - 285, wy, w - 15, wy + 28, bg_color=(0, 0, 160), border_color=(0, 0, 255), alpha=0.85)
                    cv2.putText(frame, f"! {err_msg}", (w - 275, wy + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2, cv2.LINE_AA)

        # =========================================================
        # HUD KIRI ATAS: KARTU REPETISI & STATUS LATIHAN
        # =========================================================
        draw_glass_card(frame, 15, 15, 260, 118, bg_color=(15, 20, 35), border_color=(0, 240, 255), alpha=0.75)
        cv2.putText(frame, f"EXERCISE: {exercise.upper()}", (25, 38),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 240, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, f"REPS: {tracker.counter}", (25, 76),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.15, (255, 255, 255), 2, cv2.LINE_AA)
        
        stage_color = (0, 255, 128) if tracker.stage == "UP" else (0, 165, 255)
        cv2.putText(frame, f"STAGE: {tracker.stage}  |  {fps_display:.0f} FPS", (25, 104),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, stage_color, 2, cv2.LINE_AA)

        # Tampilkan video
        cv2.imshow("Fitness Tracking Eye - Simulator", frame)

        if writer:
            writer.write(frame)

        # =========================================================
        # REAL-TIME PACING: Menghindari Video Terasa "Slow-Motion"
        # =========================================================
        # Sinkronisasi durasi frame dengan wall-clock real-time
        if video_path:
            next_frame_time = video_start_time + (expected_frame_idx / video_fps)
            delay_sec = next_frame_time - time.perf_counter()
            wait_ms = max(1, int(delay_sec * 1000)) if delay_sec > 0.001 else 1
        else:
            wait_ms = 1

        if cv2.waitKey(wait_ms) & 0xFF == ord('q'):
            break

    cap.release()
    if writer:
        writer.release()
    cv2.destroyAllWindows()
    print("[Simulator] Sesi simulasi selesai.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fitness Tracking Eye - Video Simulator")
    parser.add_argument("--video", type=str, default=None, help="Path ke berkas video .mp4 latihan")
    parser.add_argument("--exercise", type=str, default="push_up", 
                        choices=["push_up", "squat_jump", "pull_up", "sit_up", "vertical_jump"],
                        help="Jenis latihan yang dievaluasi")
    parser.add_argument("--loop", action="store_true", default=True, help="Putar ulang video secara terus-menerus")
    parser.add_argument("--no-ws", action="store_true", help="Nonaktifkan streaming WebSocket")
    parser.add_argument("--save-output", type=str, default=None, help="Path untuk menyimpan hasil video review .mp4")

    args = parser.parse_args()
    run_simulator(
        video_path=args.video,
        exercise=args.exercise,
        loop=args.loop,
        enable_ws=not args.no_ws,
        save_output=args.save_output
    )
