[CmdletBinding()]
param(
  [string[]] $Targets = @('codex'),
  [Parameter(Mandatory=$true)][string] $Repo,
  [string] $Ref = 'main',
  [string] $ArchiveSha256,
  [switch] $Quiet
)

& (Join-Path $PSScriptRoot 'install\web.ps1') -Targets $Targets -Repo $Repo -Ref $Ref -ArchiveSha256 $ArchiveSha256 -Quiet:$Quiet
exit $LASTEXITCODE
