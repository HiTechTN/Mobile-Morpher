@echo off
REM Mobile-Morpher - Installation Native Windows (Sans Docker)
REM Ce script installe toutes les dépendances directement sur votre système Windows

echo ==========================================
echo   Mobile-Morpher - Installation Windows
echo ==========================================
echo.

REM Vérifier si exécuté en tant qu'administrateur
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Ce script nécessite des droits administrateur.
    echo Veuillez cliquer droit et sélectionner "Exécuter en tant qu'administrateur"
    pause
    exit /b 1
)

REM Variables d'environnement
set "PROJECT_DIR=%USERPROFILE%\Mobile-Morpher"
set "PYTHON_DIR=%PROJECT_DIR%\venv"
set "DATA_DIR=%PROJECT_DIR%\data"

echo Répertoire du projet: %PROJECT_DIR%
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installation...
    echo.
    echo Veuillez installer Python 3.10+ depuis:
    echo https://www.python.org/downloads/
    echo.
    echo Cochez "Add Python to PATH" pendant l'installation.
    pause
    exit /b 1
)

echo ✓ Python trouvé

REM Créer le répertoire du projet
if not exist "%PROJECT_DIR%" mkdir "%PROJECT_DIR%"
cd /d "%PROJECT_DIR%"

echo.
echo Installation des outils Android...

REM Télécharger Apktool
if not exist "apktool.bat" (
    echo Téléchargement d'Apktool...
    powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat' -OutFile 'apktool.bat'"
    powershell -Command "Invoke-WebRequest -Uri 'https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar' -OutFile 'apktool.jar'"
)
echo ✓ Apktool installé

REM Télécharger Apksigner (version portable)
if not exist "apksigner.exe" (
    echo Téléchargement d'Apksigner...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/patrickfav/apksigner-mac-linux-windows/releases/download/v0.9.3/apksigner.exe' -OutFile 'apksigner.exe'" 2>nul || echo Note: Apksigner sera installée avec le SDK
)

REM Vérifier Java (nécessaire pour Apksigner)
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Java n'est pas installé. Installation...
    echo Veuillez installer JDK 17 depuis:
    echo https://adoptium.net/
    echo.
    pause
)

echo ✓ Java trouvé

echo.
echo Création de l'environnement Python virtuel...
python -m venv venv

echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Installation des dépendances Python...
pip install --upgrade pip
pip install fastapi uvicorn python-multipart pydantic

echo.
echo ==========================================
echo   Installation terminée!
echo ==========================================
echo.
echo Pour démarrer Mobile-Morpher, exécutez:
echo   cd %PROJECT_DIR%
echo   venv\Scripts\activate.bat
echo   uvicorn main:app --host 0.0.0.0 --port 9000
echo.
echo OU utilisez le fichier run.bat fourni
echo.

REM Créer un script de lancement
echo @echo off > run.bat
echo cd /d "%%~dp0" >> run.bat
echo call venv\Scripts\activate.bat >> run.bat
echo uvicorn main:app --host 0.0.0.0 --port 9000 >> run.bat
echo uvicorn main:app --host 0.0.0.0 --port 8000 >> run.bat

echo Script run.bat créé.

echo.
set /p START="Voulez-vous démarrer Mobile-Morpher maintenant? (O/n): "
if /i "%START%"=="O" (
    call venv\Scripts\activate.bat
    uvicorn main:app --host 0.0.0.0 --port 9000
)

pause