# Folder Dataset Video Pengujian (Benchmark Videos)

Silakan simpan file video rekaman latihan (.mp4) di dalam folder ini untuk pengujian simulator AI:

1. `push_up_sample.mp4` (Tampak samping / sagittal view)
2. `squat_sample.mp4` (Tampak samping atau 45 derajat)
3. `pull_up_sample.mp4` (Tampak depan / frontal view)
4. `sit_up_sample.mp4` (Tampak samping)
5. `vertical_jump_sample.mp4` (Tampak samping)

### Cara Menjalankan Simulator:
```bash
# Contoh pengujian video squat:
python src/sensors/camera/video_simulator.py --video data/videos/squat_sample.mp4 --exercise squat_jump

# Contoh pengujian video push up:
python src/sensors/camera/video_simulator.py --video data/videos/push_up_sample.mp4 --exercise push_up

# Menggunakan webcam langsung (jika tanpa argumen --video):
python src/sensors/camera/video_simulator.py --exercise squat_jump
```
