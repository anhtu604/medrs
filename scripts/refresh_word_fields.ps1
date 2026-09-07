[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string] $Source,
  [Parameter(Mandatory = $true)][string] $Output,
  [string] $Pdf
)

$ErrorActionPreference = 'Stop'
$sourcePath = [IO.Path]::GetFullPath($Source)
$outputPath = [IO.Path]::GetFullPath($Output)
if ($sourcePath -eq $outputPath) { throw 'Source and output must be different paths.' }
if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) { throw "Source DOCX not found: $sourcePath" }
if ([IO.Path]::GetExtension($outputPath).ToLowerInvariant() -ne '.docx') { throw 'Output must use the .docx extension.' }

$outputDirectory = Split-Path -Parent $outputPath
New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
Copy-Item -LiteralPath $sourcePath -Destination $outputPath -Force

$word = $null
$document = $null
$refreshFailed = $false
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $document = $word.Documents.Open($outputPath, $false, $false)

  foreach ($toc in @($document.TablesOfContents)) { $toc.Update() }
  foreach ($tof in @($document.TablesOfFigures)) { $tof.Update() }
  foreach ($story in @($document.StoryRanges)) {
    $range = $story
    while ($null -ne $range) {
      if ($range.Fields.Count -gt 0) { [void] $range.Fields.Update() }
      $range = $range.NextStoryRange
    }
  }
  [void] $document.Repaginate()
  $document.Save()

  $pdfPath = $null
  if ($Pdf) {
    $pdfPath = [IO.Path]::GetFullPath($Pdf)
    New-Item -ItemType Directory -Path (Split-Path -Parent $pdfPath) -Force | Out-Null
    # 17 = wdExportFormatPDF
    $document.ExportAsFixedFormat($pdfPath, 17)
  }
  $document.Close($false)
  $document = $null
  [ordered]@{
    status = 'FIELDS_REFRESHED'
    backend = 'word-com-powershell'
    output = $outputPath
    pdf = $pdfPath
  } | ConvertTo-Json -Depth 3
} catch {
  $refreshFailed = $true
  [ordered]@{
    status = 'HOST_CAPABILITY_UNAVAILABLE'
    backend = 'word-com-powershell'
    reason = $_.Exception.Message
  } | ConvertTo-Json -Depth 3
} finally {
  if ($null -ne $document) { try { $document.Close($false) } catch { Write-Warning "Word document cleanup failed: $($_.Exception.Message)" } }
  if ($null -ne $word) { try { $word.Quit() } catch { Write-Warning "Word application cleanup failed: $($_.Exception.Message)" } }
  if ($null -ne $document) { try { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) } catch {} }
  if ($null -ne $word) { try { [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) } catch {} }
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}
if ($refreshFailed) { exit 2 }
