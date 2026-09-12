$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$windowsRoot = Join-Path $projectRoot 'windows-app'
$reports = Join-Path $windowsRoot 'build'
$stage = Join-Path $env:LOCALAPPDATA 'FiMStudio-Validation-1.2.3'
New-Item -ItemType Directory -Force $stage | Out-Null
$portable = Join-Path $stage 'FiMpp-Studio-Portable-1.2.3-x64.exe'
$installer = Join-Path $stage 'FiMpp-Studio-Setup-1.2.3-x64.exe'
Copy-Item (Join-Path $reports 'release\FiMpp-Studio-Portable-1.2.3-x64.exe') $portable -Force
Copy-Item (Join-Path $reports 'release\FiMpp-Studio-Setup-1.2.3-x64.exe') $installer -Force
$results = [ordered]@{ platform=[Environment]::OSVersion.VersionString; architecture=$env:PROCESSOR_ARCHITECTURE; signed=$false; checks=@() }
foreach ($exe in @($portable,$installer)) {
    $signature = Get-AuthenticodeSignature $exe
    if ($signature.Status -ne 'NotSigned') { throw "Unexpected signature status on ${exe}: $($signature.Status)" }
}
$results.checks += 'Both requested EXEs are unsigned'
function Run-SelfTest($exe,$name) {
    $report = Join-Path $stage "$name.json"
    if (Test-Path $report) { Remove-Item $report }
    $process = Start-Process -FilePath $exe -ArgumentList @('--self-test',"--report=$report") -PassThru
    if (-not $process.WaitForExit(240000)) { Stop-Process -Id $process.Id; throw "$name timed out" }
    if (!(Test-Path $report)) { throw "$name did not write a report (exit $($process.ExitCode))" }
    Copy-Item $report (Join-Path $reports "$name.json") -Force
    $data = Get-Content $report -Raw | ConvertFrom-Json
    if (-not $data.success) { throw "$name failed: $($data.failures | ConvertTo-Json -Compress)" }
    Write-Host "$name PASSED: $($data.referenceCasesPassed) reference cases and runner tests"
}
Run-SelfTest $portable 'windows-portable-validation'
$results.checks += 'Portable self-test passed'
$installDir = Join-Path $stage 'Installed'
$process = Start-Process -FilePath $installer -ArgumentList @('/S',"/D=$installDir") -PassThru -Wait
if ($process.ExitCode -ne 0) { throw "Installer failed: $($process.ExitCode)" }
$installed = Join-Path $installDir 'FiM++ Studio.exe'
if (!(Test-Path $installed)) { throw 'Installed EXE missing' }
Run-SelfTest $installed 'windows-installed-validation'
$results.checks += 'Installer and installed self-test passed'
$results.installDirectory=$installDir
$results.installedExe=$installed
$results.success=$true
$results | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $reports 'windows-package-validation.json') -Encoding UTF8
Write-Host 'WINDOWS PACKAGE VALIDATION PASSED'
Write-Host "Installed test app: $installed"
