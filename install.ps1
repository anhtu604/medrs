[CmdletBinding()]
param(
  [string[]] $Targets = @('codex'),
  [string] $SourceRoot = $PSScriptRoot,
  [string] $UserRoot = [Environment]::GetFolderPath('UserProfile'),
  [string] $VersionRef = 'local',
  [switch] $Quiet
)

$ErrorActionPreference = 'Stop'
$PackageName = 'medical-research-skills-vn'
$SourceRoot = [IO.Path]::GetFullPath($SourceRoot)
$UserRoot = [IO.Path]::GetFullPath($UserRoot)
$Targets = @($Targets -split ',' | ForEach-Object { $_.Trim().ToLowerInvariant() } | Where-Object { $_ } | Select-Object -Unique)
$unknown = @($Targets | Where-Object { $_ -notin @('codex', 'claude', 'generic') })
if ($unknown) { throw "Unknown target(s): $($unknown -join ', '). Use codex, claude, or generic." }

$skillRoot = Join-Path $SourceRoot 'skills'
$indexPath = Join-Path $skillRoot 'index.json'
if (-not (Test-Path -LiteralPath $indexPath -PathType Leaf)) { throw "Install source has no skills/index.json: $SourceRoot" }
$index = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8 | ConvertFrom-Json
$skillNames = @($index.skills | ForEach-Object { $_.name } | Sort-Object -Unique)
if ($skillNames.Count -ne 24) { throw "Install source must contain exactly 24 indexed skills; found $($skillNames.Count)." }
foreach ($name in $skillNames) {
  if (-not (Test-Path -LiteralPath (Join-Path $skillRoot "$name\SKILL.md") -PathType Leaf)) {
    throw "Indexed skill is missing its SKILL.md: $name"
  }
}
foreach ($shared in @('coverage', 'profiles', 'schemas')) {
  if (-not (Test-Path -LiteralPath (Join-Path $SourceRoot $shared) -PathType Container)) {
    throw "Install source is missing shared resource: $shared"
  }
}

$targetFolders = @{ codex = '.codex'; claude = '.claude'; generic = '.agents' }
foreach ($target in $Targets) {
  $hostRoot = Join-Path $UserRoot $targetFolders[$target]
  $skillsDestination = Join-Path $hostRoot 'skills'
  $supportDestination = Join-Path $hostRoot $PackageName
  $manifestPath = Join-Path $hostRoot "$PackageName.install.json"
  $stage = Join-Path $hostRoot (".$PackageName-stage-" + [Guid]::NewGuid().ToString('N'))
  $backup = Join-Path $stage 'backup'
  $activated = @()
  $backedUp = @()
  New-Item -ItemType Directory -Path (Join-Path $stage 'skills') -Force | Out-Null
  try {
    foreach ($name in $skillNames) {
      $stagedSkill = Join-Path $stage "skills\$name"
      Copy-Item -LiteralPath (Join-Path $skillRoot $name) -Destination $stagedSkill -Recurse -Force
      $entry = Join-Path $stagedSkill 'SKILL.md'
      $text = Get-Content -LiteralPath $entry -Raw -Encoding UTF8
      $text = $text.Replace('../../coverage/', "../../$PackageName/coverage/")
      $text = $text.Replace('../../profiles/', "../../$PackageName/profiles/")
      [IO.File]::WriteAllText($entry, $text, (New-Object Text.UTF8Encoding $false))
      $head = [IO.File]::ReadAllBytes($entry) | Select-Object -First 3
      if (($head -join ',') -ne '45,45,45') { throw "Skill frontmatter encoding failed: $name" }
    }
    foreach ($shared in @('coverage', 'profiles', 'schemas')) {
      Copy-Item -LiteralPath (Join-Path $SourceRoot $shared) -Destination (Join-Path $stage $shared) -Recurse -Force
    }
    if ((Get-ChildItem -LiteralPath (Join-Path $stage 'skills') -Directory).Count -ne 24) {
      throw 'Staging validation failed: expected 24 skill directories.'
    }

    New-Item -ItemType Directory -Path $skillsDestination -Force | Out-Null
    New-Item -ItemType Directory -Path $backup -Force | Out-Null
    if (Test-Path -LiteralPath $supportDestination) {
      Move-Item -LiteralPath $supportDestination -Destination (Join-Path $backup 'support')
    }
    foreach ($name in $skillNames) {
      $destination = Join-Path $skillsDestination $name
      if (Test-Path -LiteralPath $destination) {
        Move-Item -LiteralPath $destination -Destination (Join-Path $backup $name)
        $backedUp += $name
      }
      Move-Item -LiteralPath (Join-Path $stage "skills\$name") -Destination $destination
      $activated += $name
    }
    New-Item -ItemType Directory -Path $supportDestination -Force | Out-Null
    foreach ($shared in @('coverage', 'profiles', 'schemas')) {
      Move-Item -LiteralPath (Join-Path $stage $shared) -Destination (Join-Path $supportDestination $shared)
    }
    $manifest = [ordered]@{
      package = $PackageName
      version_ref = $VersionRef
      target = $target
      installed_at = [DateTimeOffset]::Now.ToString('o')
      source_root = $SourceRoot
      skills = $skillNames
      support_path = $supportDestination
    } | ConvertTo-Json -Depth 5
    [IO.File]::WriteAllText($manifestPath, $manifest, (New-Object Text.UTF8Encoding $false))
    if (-not $Quiet) { Write-Host "Installed $PackageName for $target -> $skillsDestination" -ForegroundColor Green }
  } catch {
    foreach ($name in $activated) {
      $destination = Join-Path $skillsDestination $name
      if (Test-Path -LiteralPath $destination) { Remove-Item -LiteralPath $destination -Recurse -Force }
    }
    foreach ($name in $backedUp) {
      $destination = Join-Path $skillsDestination $name
      $saved = Join-Path $backup $name
      if (Test-Path -LiteralPath $saved) { Move-Item -LiteralPath $saved -Destination $destination }
    }
    $savedSupport = Join-Path $backup 'support'
    if (Test-Path -LiteralPath $supportDestination) { Remove-Item -LiteralPath $supportDestination -Recurse -Force }
    if (Test-Path -LiteralPath $savedSupport) { Move-Item -LiteralPath $savedSupport -Destination $supportDestination }
    throw
  } finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue }
  }
}

if (-not $Quiet) { Write-Host 'Done. Start a new AI session so it reloads the skills.' -ForegroundColor Cyan }
