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
$ExpectedSkillCount = $null
$inventoryPath = Join-Path $PSScriptRoot 'config/canonical-skills.yaml'
if (Test-Path -LiteralPath $inventoryPath -PathType Leaf) {
  $countMatch = [regex]::Match((Get-Content -LiteralPath $inventoryPath -Raw -Encoding UTF8), '(?m)^final_count:\s*(\d+)\s*$')
  if ($countMatch.Success) { $ExpectedSkillCount = [int] $countMatch.Groups[1].Value }
}
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
  if ($null -ne $ExpectedSkillCount -and @($manifest.skills).Count -ne $ExpectedSkillCount) {
    $problems += "${target}: manifest does not list $ExpectedSkillCount skills"
  }
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
