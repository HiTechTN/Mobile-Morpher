@echo off
echo Mobile-Morpher - Installation Windows
echo ========================================

REM Vérifier Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker n'est pas installé. Veuillez installer Docker Desktop.
    pause
    exit /b 1
)

REM Cloner le projet
if not exist "Mobile-Morpher" (
    git clone https://github.com/HiTechTN/Mobile-Morpher.git
    cd Mobile-Morpher
) else (
    cd Mobile-Morpher
    git pull
)

REM Lancer avec Docker Compose
echo Lancement des services...
docker compose up -d

echo.
echo ✓ Installation terminée!
echo ✓ Interface Web: http://localhost:9001
echo ✓ API Docs: http://localhost:9000/docs
pause
