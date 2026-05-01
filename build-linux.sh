#!/bin/bash
# Mobile-Morpher - Build Script Linux
# Crée un package portable pour Linux

set -e

VERSION="1.0.1"
OUTPUT_DIR="releases/linux"
PACKAGE_NAME="mobile-morpher-${VERSION}-linux-x64"

echo "=== Building Mobile-Morpher for Linux ==="

mkdir -p "$OUTPUT_DIR"

# Copier les fichiers nécessaires
echo "Copie des fichiers..."

# API Service
mkdir -p "${PACKAGE_NAME}/api"
cp -r api-service/main.py "${PACKAGE_NAME}/api/"
cp -r api-service/core "${PACKAGE_NAME}/api/"
cp -r api-service/morpher "${PACKAGE_NAME}/api/"
cp -r api-service/ai_engine "${PACKAGE_NAME}/api/"
cp api-service/requirements.txt "${PACKAGE_NAME}/api/" 2>/dev/null || true

# Create requirements.txt if not exists
cat > "${PACKAGE_NAME}/api/requirements.txt" << 'EOF'
fastapi==0.109.0
uvicorn==0.27.0
python-multipart==0.0.6
pydantic==2.5.3
httpx==0.26.0
EOF

# Web UI (Next.js bundle)
mkdir -p "${PACKAGE_NAME}/web"
cp -r web-ui/pages "${PACKAGE_NAME}/web/"
cp -r web-ui/styles "${PACKAGE_NAME}/web/"
cp web-ui/package.json "${PACKAGE_NAME}/web/"
cp web-ui/next.config.js "${PACKAGE_NAME}/web/"

# Scripts
cp install-native.sh "${PACKAGE_NAME}/"
cp install.sh "${PACKAGE_NAME}/"

# README
cp README.md "${PACKAGE_NAME}/"
cp INSTALL.md "${PACKAGE_NAME}/"

# Données
mkdir -p "${PACKAGE_NAME}/data"

# Make run script
cat > "${PACKAGE_NAME}/run.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"

# Start API in background
cd api
source ../venv/bin/activate 2>/dev/null || true
uvicorn main:app --host 0.0.0.0 --port 9000 &
API_PID=$!

echo "Mobile-Morpher API started on port 9000"
echo "PID: $API_PID"

# Keep running
wait $API_PID
EOF
chmod +x "${PACKAGE_NAME}/run.sh"

echo "Création de l'archive..."

# Créer l'archive tar.gz
cd releases/linux
tar -czf "${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}"

# Créer le ZIP pour Windows
cd ..
cd ..
zip -r "releases/linux/${PACKAGE_NAME}.zip" "releases/linux/${PACKAGE_NAME}"

echo "=== Build terminé ==="
echo "Fichiers créés:"
ls -lh "releases/linux/"