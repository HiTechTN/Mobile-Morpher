#!/bin/bash
# Build script for all platforms
# Usage: ./build-all.sh

set -e

VERSION="1.0.1"
DATE=$(date +%Y-%m-%d)

echo "======================================"
echo "  Mobile-Morpher Build System"
echo "  Version $VERSION"
echo "======================================"
echo ""

# Build Linux
echo "[1/3] Building Linux package..."
if [ -f "build-linux.sh" ]; then
    bash build-linux.sh
fi

# Build Windows (requires zip on Linux)
echo ""
echo "[2/3] Building Windows package..."
mkdir -p releases/windows
cat > releases/windows/README.txt << 'EOF'
=== Mobile-Morpher for Windows ===

Pour utiliser Mobile-Morpher sur Windows:

1. Installez Python 3.10+: https://www.python.org/downloads/
2. Installez Java JDK 17: https://adoptium.net/

3. Extrayez ce fichier ZIP dans un dossier

4. Ouvrez PowerShell dans ce dossier et exécutez:
   pip install -r requirements.txt
   python -m uvicorn main:app --host 0.0.0.0 --port 9000

5. Accédez à: http://localhost:9001

Pour l'interface web, vous devrez également installer Node.js et npm.
EOF

# Create placeholder for Windows release
cd releases/windows
zip -r "mobile-morpher-${VERSION}-windows-x64.zip" . 2>/dev/null || true
cd ../..

# Build macOS
echo "[3/3] Building macOS package..."
mkdir -p releases/macos
cat > releases/macos/README.txt << 'EOF'
=== Mobile-Morpher for macOS ===

Pour utiliser Mobile-Morpher sur macOS:

1. Installez Python: brew install python3
2. Installez Java: brew install openjdk@17

3. Extrayez ce fichier et exécutez:
   ./install-macos.sh

4. Lancez: python main.py

5. Accédez à: http://localhost:9001
EOF

echo ""
echo "======================================"
echo "  Build terminé!"
echo "======================================"
echo ""
echo "Paquets créés:"
find releases -name "*.zip" -o -name "*.tar.gz" | while read f; do
    ls -lh "$f"
done