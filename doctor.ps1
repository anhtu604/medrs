[CmdletBinding()]
param(
  [string[]] $Targets = @('codex'),
  [string] $UserRoot = [Environment]::GetFolderPath('UserProfile'),
  [switch] $Quiet
)

$PackageName = 'medical-research-skills-vn'
$UserRoot = [IO.Path]::GetFullPath($UserRoot)
$Targets = @($Targets -split ',' | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ } | Select-Object -Unique)
$targetFolders = @{ codex = '.codex'; claude = '.claude'; generic = '.agents' }
$problems = @()
foreach ($target in $Targets) {
  if (-not $targetFolders.ContainsKey($target)) { $problems += "Unknown target: $target"; continue }
  $hostRoot = Join-Path $UserRoot $targetFolders[$target]
  $manifestPath = Join-Path $hostRoot "$PackageName.install.json"
  if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    $problems += "${target}: install manifest missing"
    continue
  }
  try { $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json }
  catch { $problems += "${target}: install manifest invalid"; continue }
  if (@($manifest.skills).Count -ne 24) { $problems += "${target}: manifest does not list 24 skills" }
  foreach ($name in $manifest.skills) {
    if (-not (Test-Path -LiteralPath (Join-Path $hostRoot "skills\$name\SKILL.md") -PathType Leaf)) {
      $problems += "${target}: missing skill $name"
    }
  }
  foreach ($shared in @('coverage', 'profiles', 'schemas')) {
    if (-not (Test-Path -LiteralPath (Join-Path $hostRoot "$PackageName\$shared") -PathType Container)) {
      $problems += "${target}: missing shared resource $shared"
    }
  }
}
if ($problems) {
  if (-not $Quiet) { $problems | ForEach-Object { Write-Host "[FAIL] $_" -ForegroundColor Red } }
  exit 1
}
if (-not $Quiet) { Write-Host 'Installation health check passed.' -ForegroundColor Green }
exit 0
