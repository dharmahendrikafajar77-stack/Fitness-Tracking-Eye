@echo off
cd /d "%~dp0"
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

if not "%~1"=="" goto RUN_WITH_ARGS

echo ====================================================================
echo  FITNESS TRACKING EYE - DUAL-VIEW MULTI-CAMERA FUSION SIMULATOR
echo ====================================================================
echo  Memuat video dual-view: PushUpPV1 dan PushUpPV2...
echo.
echo  Pilihan latihan lain:
echo    .\run_dual_simulator.bat --exercise sit_up
echo    .\run_dual_simulator.bat --exercise squat_jump
echo    .\run_dual_simulator.bat --exercise vertical_jump
echo ====================================================================
"%PYTHON_EXE%" src/sensors/camera/dual_view_simulator.py --exercise push_up
goto END

:RUN_WITH_ARGS
"%PYTHON_EXE%" src/sensors/camera/dual_view_simulator.py %*

:END
pause
