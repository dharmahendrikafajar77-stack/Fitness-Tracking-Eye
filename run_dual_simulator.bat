@echo off
cd /d "%~dp0"
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

if "%~1"=="" (
    echo ====================================================================
    echo  FITNESS TRACKING EYE - DUAL-VIEW MULTI-CAMERA SIMULATOR (DEMO MODE)
    echo ====================================================================
    echo  Format penggunaan video Anda nanti:
    echo    .\run_dual_simulator.bat --cam1 data/videos/side.mp4 --start1 3.5 --cam2 data/videos/front.mp4 --start2 8.2 --exercise push_up
    echo ====================================================================
    "%PYTHON_EXE%" src/sensors/camera/dual_view_simulator.py --cam1 data/videos/12341234.mp4 --exercise push_up
) else (
    "%PYTHON_EXE%" src/sensors/camera/dual_view_simulator.py %*
)
pause
