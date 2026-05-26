# Asso Lab — full briefing cycle in one command.
# Usage: .\run.ps1   (or  pwsh -File .\run.ps1)
#
#  1. Load .env into the current PowerShell session.
#  2. Run briefing_orchestrator_v0.py.
#  3. If it exits non-zero -> show the code and stop.
#  4. Display the generated .md.
#  5. Prompt "Publier ? (o/n)".
#  6. 'n' -> "Reste en DRAFT. Fin." and stop.
#  7. 'o' -> open .md in notepad for copy/paste, mark receipt PUBLISHED,
#           commit, then prompt "Push ? (o/n)". 'o' pushes, 'n' stops local.

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

# --- 1. Load .env ---
if (-not (Test-Path .env)) {
    Write-Host ".env not found. Copy .env.example and set GEMINI_API_KEY." -ForegroundColor Red
    exit 1
}

foreach ($line in Get-Content .env) {
    $trimmed = $line.Trim()
    if (-not $trimmed -or $trimmed.StartsWith('#')) { continue }
    $idx = $trimmed.IndexOf('=')
    if ($idx -lt 1) { continue }
    $key = $trimmed.Substring(0, $idx).Trim()
    $val = $trimmed.Substring($idx + 1).Trim().Trim('"').Trim("'")
    Set-Item -Path "env:$key" -Value $val
}

# --- 2. Run orchestrator ---
Write-Host ""
Write-Host "Running briefing_orchestrator_v0.py..." -ForegroundColor Cyan
python briefing_orchestrator_v0.py
$orchExit = $LASTEXITCODE

# --- 3. Exit on failure ---
if ($orchExit -ne 0) {
    Write-Host "Orchestrator failed (exit code $orchExit). Stop." -ForegroundColor Red
    exit $orchExit
}

# Locate today's files (UTC, matches the orchestrator).
$today       = (Get-Date).ToUniversalTime().ToString('yyyy-MM-dd')
$notePath    = "publications/$today-briefing.md"
$receiptPath = "receipts/$today-receipt.json"

if (-not (Test-Path $notePath)) {
    Write-Host "Briefing not found at $notePath. Stop." -ForegroundColor Red
    exit 1
}

# --- 4. Show .md ---
Write-Host ""
Write-Host "=== BRIEFING $today ===" -ForegroundColor Cyan
Get-Content $notePath -Raw
Write-Host "=== END ===" -ForegroundColor Cyan
Write-Host ""

# --- 5. First gate: publish? ---
$publish = Read-Host "Publier ? (o/n)"

# --- 6. Negative branch ---
if ($publish -ne 'o') {
    Write-Host "Reste en DRAFT. Fin." -ForegroundColor Yellow
    exit 0
}

# --- 7a. Open in notepad ---
Start-Process notepad.exe $notePath

# --- 7b. Receipt status DRAFT -> PUBLISHED ---
# Done via python so JSON formatting matches the orchestrator's output
# (indent=2, ensure_ascii=False). ConvertTo-Json would reformat noisily.
python -c "import json, pathlib; p = pathlib.Path(r'$receiptPath'); r = json.loads(p.read_text(encoding='utf-8')); r['status'] = 'PUBLISHED'; p.write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding='utf-8')"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Receipt status update failed." -ForegroundColor Red
    exit 1
}

# --- 7c. git add + commit ---
git add $receiptPath
if ($LASTEXITCODE -ne 0) { Write-Host "git add failed" -ForegroundColor Red; exit 1 }

git commit -m "Receipt $today — PUBLISHED"
if ($LASTEXITCODE -ne 0) { Write-Host "git commit failed" -ForegroundColor Red; exit 1 }

Write-Host "Receipt committe localement." -ForegroundColor Green
Write-Host ""

# --- 7d. Second gate: push? ---
$pushAns = Read-Host "Push ? (o/n)"

# --- 7e/f. Push or stop ---
if ($pushAns -ne 'o') {
    Write-Host "Stop. Commit reste local." -ForegroundColor Yellow
    exit 0
}

git push origin main
if ($LASTEXITCODE -ne 0) { Write-Host "git push failed" -ForegroundColor Red; exit 1 }

Write-Host ""
Write-Host "Done. Pushed to origin/main." -ForegroundColor Green
