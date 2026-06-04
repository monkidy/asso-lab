# setup_x_env.ps1
# Cree le fichier .env.x (cles API X pour Proof of Agent) avec des placeholders.
# Tu le lances UNE fois, puis tu ouvres .env.x et tu colles tes valeurs.
# Les secrets restent en local : .env.x est gitignore, jamais commit, jamais transmis a Claude.

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$envFile = Join-Path $root ".env.x"

if (Test-Path $envFile) {
    Write-Host ".env.x existe deja. Je n'ecrase rien." -ForegroundColor Yellow
} else {
    $template = @'
# === Cles API X pour Proof of Agent ===
# NE JAMAIS COMMIT CE FICHIER. Remplace les valeurs apres le = (sans guillemets, sans espaces).
#
# Tu as deja : API key (clef consommateur), API secret, Bearer token.
# IMPORTANT : pour PUBLIER un tweet, le Bearer token ne suffit PAS.
# Il te faut AUSSI Access Token + Access Token Secret, generes avec la permission
# d'app "Read and Write" :
#   Dev portal X > ton app > User authentication settings > Read and Write,
#   PUIS Keys and tokens > Access Token and Secret > Generate.
# Si tu avais genere l'access token AVANT de passer en Read and Write, regenere-le.

X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
X_BEARER_TOKEN=
'@
    Set-Content -Path $envFile -Value $template -Encoding utf8
    Write-Host ".env.x cree dans $root" -ForegroundColor Green
}

# Securite : verifier que .env.x est bien ignore par git
try { $ignored = git -C $root check-ignore ".env.x" 2>$null } catch { $ignored = $null }
if ($ignored) {
    Write-Host "OK : .env.x est ignore par git. Tes secrets ne partiront jamais en public." -ForegroundColor Green
} else {
    Write-Host "ATTENTION : .env.x n'est PAS ignore par git. Ne commit rien avant de corriger le .gitignore." -ForegroundColor Red
}

Write-Host ""
Write-Host "Etape suivante : ouvre .env.x, colle tes valeurs, sauvegarde. Termine."
