param([string]$CodexHome = '')
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ([string]::IsNullOrWhiteSpace($CodexHome)) {
    $CodexHome = $env:CODEX_HOME
    if ([string]::IsNullOrWhiteSpace($CodexHome)) {
        $CodexHome = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
    }
}

# Check the entire bundle before changing the destination.
$lines = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'SHA256SUMS')
foreach ($line in $lines) {
    if ($line -notmatch '^([0-9a-f]{64})  (pets/(cheese|cream)/(pet\.json|spritesheet\.webp))$') {
        throw "Invalid checksum entry: $line"
    }
    $expected = $Matches[1]
    $file = Join-Path $PSScriptRoot $Matches[2]
    if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expected) {
        throw "Checksum mismatch: $file. Download and extract the ZIP again."
    }
}
if ($lines.Count -ne 4) { throw 'Expected four pet files in SHA256SUMS.' }
$petsRoot = Join-Path $CodexHome 'pets'
foreach ($petId in @('cheese', 'cream')) {
    $target = Join-Path $petsRoot $petId
    if (Test-Path -LiteralPath $target) {
        if ((Get-Item -LiteralPath $target).Attributes -band [IO.FileAttributes]::ReparsePoint) {
            throw "Refusing linked destination: $target"
        }
    }
}
$backupDir = $null
foreach ($petId in @('cheese', 'cream')) {
    $source = Join-Path (Join-Path $PSScriptRoot 'pets') $petId
    $target = Join-Path $petsRoot $petId
    if (Test-Path -LiteralPath $target) {
        if ($null -eq $backupDir) {
            $backupDir = Join-Path (Join-Path $CodexHome 'pet-backups') ('cat-pets-' + [Guid]::NewGuid().ToString('N'))
            New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        }
        Copy-Item -LiteralPath $target -Destination (Join-Path $backupDir $petId) -Recurse
    }
    New-Item -ItemType Directory -Path $target -Force | Out-Null
    foreach ($name in @('pet.json', 'spritesheet.webp')) {
        $sourceFile = Join-Path $source $name
        $targetFile = Join-Path $target $name
        Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
        if ((Get-FileHash -LiteralPath $sourceFile).Hash -ne (Get-FileHash -LiteralPath $targetFile).Hash) {
            throw "Installed file verification failed: $targetFile"
        }
    }
}
Write-Host "Installed Cheese and Cream in: $petsRoot"
if ($null -ne $backupDir) { Write-Host "Previous files backed up in: $backupDir" }
Write-Host 'Open Codex > Settings > Pets and choose Cheese or Cream.'
Write-Host 'If they are missing, quit and reopen Codex.'
