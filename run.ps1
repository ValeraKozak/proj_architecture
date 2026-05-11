param(
    [switch]$SkipInstall,
    [switch]$ForceInstall
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $projectRoot "frontend"
$envFile = Join-Path $projectRoot ".env"
$envExampleFile = Join-Path $projectRoot ".env.example"
$frontendModulesDir = Join-Path $frontendDir "node_modules"
$venvRoot = Join-Path $env:LOCALAPPDATA "proj_architecture_l3_venv"
$pythonExe = Join-Path $venvRoot "Scripts\python.exe"
$activateScript = Join-Path $venvRoot "Scripts\Activate.ps1"
$backendMarker = Join-Path $venvRoot ".backend-deps-installed"
$frontendMarker = Join-Path $frontendDir ".frontend-deps-installed"

if (-not (Test-Path $pythonExe)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    if (-not (Test-Path $venvRoot)) {
        New-Item -ItemType Directory -Path $venvRoot -Force | Out-Null
    }

    Push-Location $venvRoot
    try {
        py -3.14 -m venv $venvRoot
    }
    finally {
        Pop-Location
    }
}

if (-not (Test-Path $activateScript)) {
    throw "Activation script not found at $activateScript"
}

try {
    & $pythonExe -m pip --version | Out-Null
}
catch {
    throw "pip is not available in the virtual environment at $venvRoot"
}

$backendInstalled = $false
try {
    & $pythonExe -m pip show bulletin-board-platform | Out-Null
    $backendInstalled = $true
}
catch {
    $backendInstalled = $false
}

if (-not (Test-Path (Join-Path $frontendDir "package.json"))) {
    throw "Frontend package.json not found."
}

if (-not (Test-Path $envFile)) {
    if (-not (Test-Path $envExampleFile)) {
        throw ".env.example not found. Cannot create local environment file."
    }

    Write-Host "Creating .env from .env.example..." -ForegroundColor Cyan
    Copy-Item $envExampleFile $envFile
}

if ($backendInstalled -and -not (Test-Path $backendMarker)) {
    Set-Content -Path $backendMarker -Value "ok"
}

if ((Test-Path $frontendModulesDir) -and -not (Test-Path $frontendMarker)) {
    Set-Content -Path $frontendMarker -Value "ok"
}

if (-not $SkipInstall -and ((-not $backendInstalled) -or (-not (Test-Path $backendMarker)) -or $ForceInstall)) {
    Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
    Push-Location $projectRoot
    try {
        & $pythonExe -m pip install -e ".[dev]"
        Set-Content -Path $backendMarker -Value "ok"
    }
    finally {
        Pop-Location
    }
}

if (-not $SkipInstall -and ((-not (Test-Path $frontendModulesDir)) -or (-not (Test-Path $frontendMarker)) -or $ForceInstall)) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location $frontendDir
    try {
        npm install
        Set-Content -Path $frontendMarker -Value "ok"
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
