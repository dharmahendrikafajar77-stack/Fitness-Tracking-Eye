import cv2
import mediapipe as mp
import numpy as np

# Inisialisasi MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def calculate_angle(a, b, c):
    """
    Menghitung sudut antara 3 titik koordinat (A, B, C) dimana B adalah titik sudutnya.
    """
    a = np.array(a) # Titik pertama (misal: Pinggul)
    b = np.array(b) # Titik tengah/sudut (misal: Lutut)
    c = np.array(c) # Titik akhir (misal: Pergelangan kaki)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

def main():
    # Buka webcam lokal (0 biasanya adalah webcam default laptop)
    cap = cv2.VideoCapture(0)
    
    # Variabel State Machine untuk menghitung Squat
    counter = 0 
    stage = None # Bisa "UP" (berdiri) atau "DOWN" (jongkok)
    
    print("Memulai Kamera... Tekan 'q' pada keyboard untuk keluar.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame kamera.")
            break
            
        # Ubah warna BGR (standar OpenCV) ke RGB (dibutuhkan oleh MediaPipe)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Jalankan Pose Estimation (AI)
        results = pose.process(image)
    
        # Ubah kembali ke BGR untuk ditampilkan di layar
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Ekstrak landmarks (titik tulang)
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Ambil koordinat untuk Kaki Kiri (Pinggul, Lutut, Pergelangan Kaki)
            # Indeks MediaPipe: 23 = Hip, 25 = Knee, 27 = Ankle
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            # Konversi koordinat relatif (0-1) ke piksel layar untuk menggambar teks
            h, w, _ = image.shape
            knee_px = tuple(np.multiply(knee, [w, h]).astype(int))
            
            # Hitung Sudut Lutut
            angle = calculate_angle(hip, knee, ankle)
            
            # Visualisasikan Sudut di Lutut
            cv2.putText(image, str(int(angle)), 
                           knee_px, 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            # STATE MACHINE LOGIC UNTUK MENGHITUNG SQUAT
            # 1. Jika sudut lutut > 160 derajat, user sedang berdiri (UP)
            if angle > 160:
                stage = "UP"
            # 2. Jika sudut lutut < 90 derajat dan sebelumnya berdiri, user jongkok (DOWN), tambah skor!
            if angle < 90 and stage == 'UP':
                stage = "DOWN"
                counter += 1
                print(f"Bagus! Repetisi: {counter}")
                       
        except:
            pass # Lewati jika tubuh tidak terdeteksi
        
        # Buat Kotak Status UI di pojok kiri atas
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        # Tampilkan Jumlah Repetisi
        cv2.putText(image, 'REPS', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Tampilkan Status (UP/DOWN)
        cv2.putText(image, 'STAGE', (65,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, stage if stage else "-", 
                    (60,60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Gambar kerangka tubuh (Skeletal Overlay)
        mp_drawing.draw_landmarks(
            image, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), # Titik
            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)  # Garis
        )               
        
        # Tampilkan jendela video
        cv2.imshow('Fitness Tracking Eye - Prototype', image)

        # Keluar jika tombol 'q' ditekan
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
