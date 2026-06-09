# ACE: Setup Windows Task Scheduler
# Lance python run_pipeline.py tous les jours de semaine a 13h00 CET.
# Usage : .\setup_scheduler.ps1
# Pas besoin d'administrateur : -RunLevel Limited suffit pour l'utilisateur courant.

$ErrorActionPreference = 'Stop'

$RepoPath   = $PSScriptRoot

# Resout le VRAI interpreteur, jamais le shim WindowsApps (App Execution Alias),
# qui ne se comporte pas pareil en session non-interactive (Session 0) a 13h00.
$Python = (Get-Command python -All -ErrorAction SilentlyContinue |
    Where-Object { $_.Source -and $_.Source -notlike "*WindowsApps*" } |
    Select-Object -First 1).Source
if (-not $Python) {
    # Fallback : le lanceur py resout l'install reelle.
    $Python = (& py -3 -c "import sys; print(sys.executable)" 2>$null)
}
if (-not $Python -or -not (Test-Path $Python)) {
    throw "Aucun interpreteur Python reel trouve hors WindowsApps. Installe python.org ou corrige le PATH."
}

$TaskName   = "ACE Daily Pipeline"
$LogFile    = Join-Path $RepoPath "logs\scheduler.log"

# Cree le dossier logs si absent
New-Item -ItemType Directory -Force -Path (Join-Path $RepoPath "logs") | Out-Null

$Action = New-ScheduledTaskAction `
    -Execute $Python `
    -Argument "run_pipeline.py" `
    -WorkingDirectory $RepoPath

# Lundi a vendredi, 13h00
$Trigger = New-ScheduledTaskTrigger `
    -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At "13:00"

$Settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Enregistre (ou met a jour) la tache
if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Ancienne tache supprimee." -ForegroundColor Yellow
}

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -RunLevel Limited `
    -Description "ACE : brief + draft X + gate Telegram. Valide sur Asso_CM." `
    -ErrorAction Stop | Out-Null

Write-Host ""
Write-Host "Tache planifiee creee : '$TaskName'" -ForegroundColor Green
Write-Host "  Script  : $RepoPath\run_pipeline.py"
Write-Host "  Python  : $Python"
Write-Host "  Horaire : lundi-vendredi, 13h00"
Write-Host ""
Write-Host "Pour tester immediatement :"
Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
Write-Host ""
Write-Host "Pour voir le statut :"
Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Get-ScheduledTaskInfo"
Write-Host ""
Write-Host "Pour supprimer :"
Write-Host "  Unregister-ScheduledTask -TaskName '$TaskName'"
