[CmdletBinding()]
param(
  [string[]] $Targets = @('codex'),
  [string] $Repo = $(if ($env:MEDICAL_RESEARCH_SKILLS_REPO) { $env:MEDICAL_RESEARCH_SKILLS_REPO } else { 'anhtu604/medrs' }),
  [string] $Ref = 'main',
  [string] $ArchiveSha256,
  [switch] $Quiet
)

$ErrorActionPreference = 'Stop'
if ($Repo -notmatch '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$') { throw "Invalid GitHub repository: $Repo" }
if ([Net.ServicePointManager]::SecurityProtocol -notmatch 'Tls12') {
  [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
}

$temp = Join-Path ([IO.Path]::GetTempPath()) ('medical-research-skills-vn-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $temp -Force | Out-Null
try {
  $zip = Join-Path $temp 'repository.zip'
  $url = "https://codeload.github.com/$Repo/zip/$Ref"
  $priorProgress = $ProgressPreference
  $ProgressPreference = 'SilentlyContinue'
  try { Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing } finally { $ProgressPreference = $priorProgress }
  if ($ArchiveSha256) {
    $actual = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash
    if ($actual -ne $ArchiveSha256.ToUpperInvariant()) { throw "Archive checksum mismatch. Expected $ArchiveSha256, got $actual." }
  }
  Expand-Archive -LiteralPath $zip -DestinationPath $temp -Force
  $source = Get-ChildItem -LiteralPath $temp -Directory | Select-Object -First 1
  if (-not $source) { throw 'Downloaded archive contains no repository directory.' }
  $installer = Join-Path $source.FullName 'install.ps1'
  if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) { throw 'Downloaded repository has no install.ps1.' }
  & $installer -SourceRoot $source.FullName -Targets $Targets -VersionRef $Ref -Quiet:$Quiet
} finally {
  if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force -ErrorAction SilentlyContinue }
}
