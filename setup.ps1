# setup.ps1 - AutoResponder Full Setup for Windows

Write-Host "`n🚀 AutoResponder Setup & Launcher" -ForegroundColor Cyan

# --- 1. Check Python ---
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed. Please install Python 3.10+ and rerun this script." -ForegroundColor Red
    exit
}

# --- 2. Check Docker ---
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop and enable WSL2 integration." -ForegroundColor Red
    exit
} else {
    Write-Host "🐳 Docker found." -ForegroundColor Green
}

# --- 2.1 Build Kafka and Redis --- 
Write-Host "`n📦 Building and starting Kafka and Redis via docker-compose..." -ForegroundColor Yellow
docker-compose up --build -d


# --- 3. Check WSL and Ubuntu ---
$wslDistros = wsl.exe --list --quiet
if ($wslDistros -notmatch "Ubuntu") {
    Write-Host "❌ WSL with Ubuntu not found. Please install Ubuntu from Microsoft Store." -ForegroundColor Red
    exit
} else {
    Write-Host "🐧 Ubuntu WSL found." -ForegroundColor Green
}

# --- 4. Check filebeat.yml exists ---
$filebeatPath = "\\wsl$\Ubuntu\etc\filebeat\filebeat.yml"
if (-not (Test-Path $filebeatPath)) {
    Write-Host "⚠️  filebeat.yml not found at expected location: $filebeatPath" -ForegroundColor Yellow
    Write-Host "Make sure Filebeat is installed and configured inside your WSL Ubuntu." -ForegroundColor Yellow
    exit
} else {
    Write-Host "✅ filebeat.yml found." -ForegroundColor Green
}

# --- 5. Start Docker Compose ---
Write-Host "`n📦 Starting Kafka and Redis via docker-compose..." -ForegroundColor Yellow
docker-compose up -d

# --- 6. Set up venv ---
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated." -ForegroundColor Green

# --- 7. Install dependencies ---
Write-Host "📥 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# --- 8. Start Filebeat inside Ubuntu ---
Write-Host "`n📡 Starting Filebeat inside WSL Ubuntu..." -ForegroundColor Cyan
wsl -d Ubuntu -- sudo systemctl start filebeat
Start-Sleep -Seconds 2

# --- 9. Start Consumer Python Script ---
Write-Host "🚨 Launching AutoResponder Log Consumer (Kafka + Redis + Telegram Alerts)..." -ForegroundColor Green
python stream\consumer.py
