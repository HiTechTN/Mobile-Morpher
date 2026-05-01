#!/bin/bash
# Demo script pour les tutoriels vidéo Mobile-Morpher

echo "==========================================="
echo "  Mobile-Morpher - Démonstration Complète"
echo "==========================================="
echo ""

# Couleurs pour le terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test APK existant
TEST_APK="/tmp/test_real.apk"

if [ ! -f "$TEST_APK" ]; then
    echo -e "${YELLOW}Attention: APK de test non trouvé${NC}"
    echo "Utilisation d'un APK existant dans shared-volume..."
    TEST_APK="shared-volume/a6690b20-0d8d-466d-adf9-f984e66351ec/original.apk"
fi

echo -e "${BLUE}=== Étape 1: Vérification des services ===${NC}"
docker ps --filter "name=mobile-morpher" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo -e "${BLUE}=== Étape 2: Upload APK ===${NC}"
SESSION=$(curl -s -X POST http://localhost:9000/api/upload \
    -F "file=@$TEST_APK" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")
echo -e "Session: ${GREEN}$SESSION${NC}"
echo ""

echo -e "${BLUE}=== Étape 3: Transformation (Mode Express) ===${NC}"
curl -s -X POST "http://localhost:9000/api/process/$SESSION" \
    -H "Content-Type: application/json" \
    -d '{
        "new_app_name": "VideoPlayer",
        "new_package_id": "com.demo.player",
        "mode": "express"
    }' | python3 -m json.tool
echo ""

echo -e "${BLUE}=== Étape 4: Vérification des modifications ===${NC}"
echo "Package ID:"
grep -o 'package="[^"]*"' "shared-volume/$SESSION/decompiled/AndroidManifest.xml"
echo ""
echo "Nom de l'application:"
grep -o 'VideoPlayer' "shared-volume/$SESSION/decompiled/res/values/strings.xml"
echo ""

echo -e "${BLUE}=== Étape 5: Résultat final ===${NC}"
ls -lh "shared-volume/$SESSION/modified.apk"
echo ""

echo -e "${GREEN}✓ Démonstration terminée avec succès!${NC}"
echo ""
echo "Pour tester via l'interface web:"
echo "  1. Ouvrir http://localhost:9001"
echo "  2. Sélectionner un fichier APK"
echo "  3. Remplir le nom et le Package ID"
echo "  4. Cliquer sur 'Transformer l'APK'"