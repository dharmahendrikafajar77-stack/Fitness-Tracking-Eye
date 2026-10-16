@echo off
cd /d "%~dp0"
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

if "%~1"=="" (
    "%PYTHON_EXE%" src/sensors/camera/video_simulator.py --video data/videos/13134-245530646.mp4 --exercise push_up
) else (
    "%PYTHON_EXE%" src/sensors/camera/video_simulator.py %*
)
pause
