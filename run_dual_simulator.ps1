# Fitness Tracking Eye - PowerShell Runner for Dual-View Simulator
$pythonExe = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

if ($args.Count -eq 0) {
    Write-Host "====================================================================" -ForegroundColor Cyan
    Write-Host " FITNESS TRACKING EYE - DUAL-VIEW MULTI-CAMERA SIMULATOR (DEMO MODE)" -ForegroundColor Yellow
    Write-Host "====================================================================" -ForegroundColor Cyan
    Write-Host " Format penggunaan video Anda nanti:" -ForegroundColor Gray
    Write-Host "   .\run_dual_simulator.ps1 --cam1 data/videos/side.mp4 --start1 3.5 --cam2 data/videos/front.mp4 --start2 8.2 --exercise push_up" -ForegroundColor Green
    Write-Host "====================================================================" -ForegroundColor Cyan
    & $pythonExe src/sensors/camera/dual_view_simulator.py --cam1 data/videos/12341234.mp4 --exercise push_up
} else {
    & $pythonExe src/sensors/camera/dual_view_simulator.py @args
}
