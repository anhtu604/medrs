[CmdletBinding()]
param(
  [string[]] $Targets = @('codex'),
  [string] $UserRoot = [Environment]::GetFolderPath('UserProfile'),
  [switch] $Quiet
)

$ErrorActionPreference = 'Stop'
$PackageName = 'medical-research-skills-vn'
$UserRoot = [IO.Path]::GetFullPath($UserRoot)
$Targets = @($Targets -split ',' | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ } | Select-Object -Unique)
$targetFolders = @{ codex = '.codex'; claude = '.claude'; generic = '.agents' }
foreach ($target in $Targets) {
  if (-not $targetFolders.ContainsKey($target)) { throw "Unknown target: $target" }
  $hostRoot = Join-Path $UserRoot $targetFolders[$target]
  $manifestPath = Join-Path $hostRoot "$PackageName.install.json"
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    if (-not $Quiet) { Write-Host "No managed installation found for $target." -ForegroundColor Yellow }
    continue
  }
  $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach ($name in $manifest.skills) {
    $path = Join-Path $hostRoot "skills\$name"
    if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Recurse -Force }
  }
  $support = Join-Path $hostRoot $PackageName
  if (Test-Path -LiteralPath $support) { Remove-Item -LiteralPath $support -Recurse -Force }
  Remove-Item -LiteralPath $manifestPath -Force
  if (-not $Quiet) { Write-Host "Uninstalled $PackageName from $target." -ForegroundColor Green }
}
