# Fitness Tracking Eye - PowerShell Runner for Dual-View Simulator
$pythonExe = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pythonExe)) {
    $pythonExe = "python"
}

if ($args.Count -eq 0) {
    Write-Host "====================================================================" -ForegroundColor Cyan
    Write-Host " FITNESS TRACKING EYE - DUAL-VIEW MULTI-CAMERA FUSION SIMULATOR" -ForegroundColor Yellow
    Write-Host "====================================================================" -ForegroundColor Cyan
    Write-Host " Memuat video dual-view: PushUpPV1 (Depan) + PushUpPV2 (Samping)..." -ForegroundColor Green
    Write-Host ""
    Write-Host " Pilihan latihan lain:" -ForegroundColor Gray
    Write-Host "   .\run_dual_simulator.ps1 --exercise sit_up" -ForegroundColor White
    Write-Host "   .\run_dual_simulator.ps1 --exercise squat_jump" -ForegroundColor White
    Write-Host "   .\run_dual_simulator.ps1 --exercise vertical_jump" -ForegroundColor White
    Write-Host "====================================================================" -ForegroundColor Cyan
    & $pythonExe src/sensors/camera/dual_view_simulator.py --exercise push_up
} else {
    & $pythonExe src/sensors/camera/dual_view_simulator.py @args
}
