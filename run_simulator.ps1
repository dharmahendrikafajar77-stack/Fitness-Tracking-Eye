# Script peluncur simulator Fitness Tracking Eye
param(
    [string]$video = "data/videos/13134-245530646.mp4",
    [string]$exercise = "push_up",
    [switch]$noWs,
    [string]$saveOutput
)

$pyExe = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
if (-not (Test-Path $pyExe)) {
    $pyExe = "python"
}

$argsList = @("src/sensors/camera/video_simulator.py", "--video", $video, "--exercise", $exercise)
if ($noWs) {
    $argsList += "--no-ws"
}
if ($saveOutput) {
    $argsList += @("--save-output", $saveOutput)
}

& $pyExe $argsList
