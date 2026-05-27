param(
    [string]$PythonExe = ".\.venv\Scripts\python.exe"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path $PythonExe)) {
    throw "Python environment not found at $PythonExe. Create .venv and install dev-requirements.txt first."
}

$nsisCandidates = @(
    "${env:ProgramFiles(x86)}\NSIS\makensis.exe",
    "$env:ProgramFiles\NSIS\makensis.exe",
    "$env:LocalAppData\Programs\NSIS\makensis.exe"
)
$makensis = $nsisCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $makensis) {
    throw "NSIS is not installed. Install it with: winget install --id NSIS.NSIS -e"
}

& $PythonExe ".\scripts\generate_icon.py"
if ($LASTEXITCODE -ne 0) { throw "Icon generation failed." }

& $PythonExe -m PyInstaller --noconfirm --clean ".\DocliraPDFLite.spec"
if ($LASTEXITCODE -ne 0) { throw "Executable build failed." }

New-Item -ItemType Directory -Force ".\release_build" | Out-Null
& $makensis ".\installer\DocliraPDFLite.nsi"
if ($LASTEXITCODE -ne 0) { throw "Installer build failed." }

Write-Host "Installer complete: release_build\DocliraPDF_Lite_Setup_v0.1.0_Windows_x64.exe"
