param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"
$frontendDir = Join-Path $projectRoot "frontend"
$activateScript = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path $pythonExe)) {
    throw "Python virtual environment not found at .venv. Create it first with: py -m venv .venv"
}

if (-not (Test-Path $activateScript)) {
    throw "Activation script not found at .venv\Scripts\Activate.ps1"
}

if (-not (Test-Path (Join-Path $frontendDir "package.json"))) {
    throw "Frontend package.json not found."
}

if (-not $SkipInstall -and -not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location $frontendDir
    try {
        npm install
    }
    finally {
        Pop-Location
    }
}

$backendCommand = "& '$activateScript'; Set-Location '$projectRoot'; uvicorn src.main:app --reload"
$frontendCommand = "Set-Location '$frontendDir'; npm run dev -- --host 127.0.0.1"

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCommand | Out-Null
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCommand | Out-Null

Write-Host "Backend started in a new window: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "Frontend started in a new window: http://127.0.0.1:5173" -ForegroundColor Green
