#!/bin/bash
# Mobile-Morpher - Installation Native Linux (Sans Docker)
# Ce script installe toutes les dépendances directement sur votre système

set -e

echo "=========================================="
echo "  Mobile-Morpher - Installation Native Linux"
echo "=========================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Détecter la distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        echo $ID
    else
        echo "unknown"
    fi
}

DISTRO=$(detect_distro)
echo -e "${YELLOW}Distribution détectée: $DISTRO${NC}"

# Prérequis
check_requirements() {
    echo "Vérification des prérequis..."
    
    # Python 3
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}Python3 non trouvé. Installation...${NC}"
        case $DISTRO in
            ubuntu|debian)
                sudo apt update && sudo apt install -y python3 python3-pip python3-venv
                ;;
            fedora)
                sudo dnf install -y python3 python3-pip
                ;;
            arch)
                sudo pacman -S python python-pip
                ;;
        esac
    fi
    
    # Java JDK
    if ! command -v java &> /dev/null; then
        echo -e "${YELLOW}Java non trouvé. Installation...${NC}"
        case $DISTRO in
            ubuntu|debian)
                sudo apt install -y openjdk-17-jdk-headless
                ;;
            fedora)
                sudo dnf install -y java-17-openjdk-headless
                ;;
            arch)
                sudo pacman -S jdk17-openjdk-headless
                ;;
        esac
    fi
    
    # Outils nécessaires
    echo "Installation des outils supplémentaires..."
    case $DISTRO in
        ubuntu|debian)
            sudo apt install -y wget zipalign
            ;;
        fedora)
            sudo dnf install -y wget zip
            ;;
    esac
    
    echo -e "${GREEN}✓ Prérequis installés${NC}"
}

# Installation Apktool
install_apktool() {
    echo ""
    echo "Installation d'Apktool..."
    
    if command -v apktool &> /dev/null; then
        echo -e "${GREEN}✓ Apktool déjà installé${NC}"
        return
    fi
    
    # Télécharger Apktool
    wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool -O /tmp/apktool
    wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -O /tmp/apktool.jar
    
    sudo mv /tmp/apktool /usr/local/bin/apktool
    sudo mv /tmp/apktool.jar /usr/local/bin/apktool.jar
    sudo chmod +x /usr/local/bin/apktool
    sudo ln -sf /usr/local/bin/apktool.jar /usr/local/bin/apktool_2.9.3.jar
    
    echo -e "${GREEN}✓ Apktool installé${NC}"
}

# Installation Apksigner
install_apksigner() {
    echo ""
    echo "Installation d'Apksigner..."
    
    if command -v apksigner &> /dev/null; then
        echo -e "${GREEN}✓ Apksigner déjà installé${NC}"
        return
    fi
    
    # Apksigner fait partie d'Android SDK Build Tools
    # On utilise une version autonome
    wget -q https://github.com/patrickfav/apksigner-mac-linux-windows/releases/download/v0.9.3/apksigner -O /tmp/apksigner
    sudo mv /tmp/apksigner /usr/local/bin/apksigner
    sudo chmod +x /usr/local/bin/apksigner
    
    echo -e "${GREEN}✓ Apksigner installé${NC}"
}

# Installation des dépendances Python
install_python_deps() {
    echo ""
    echo "Installation des dépendances Python..."
    
    # Créer un虚拟环境
    python3 -m venv venv
    source venv/bin/activate
    
    # Installer les dépendances
    pip install --upgrade pip
    pip install fastapi uvicorn python-multipart pydantic
    
    echo -e "${GREEN}✓ Dépendances Python installées${NC}"
}

# Configuration du projet
setup_project() {
    echo ""
    echo "Configuration du projet..."
    
    # Créer le volume de travail
    mkdir -p ~/mobile-morpher-data
    
    # Copier les fichiers nécessaires
    if [ ! -f "main.py" ]; then
        cp -r api-service/* . 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✓ Projet configuré${NC}"
}

# Lancer l'application
start_app() {
    echo ""
    echo "Lancement de Mobile-Morpher..."
    
    source venv/bin/activate
    
    # Démarrer l'API
    uvicorn main:app --host 0.0.0.0 --port 9000 &
    API_PID=$!
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo "  Mobile-Morpher est maintenant actif!"
    echo "==========================================${NC}"
    echo ""
    echo "  📱 Interface Web: http://localhost:9001"
    echo "  🔌 API:           http://localhost:9000"
    echo "  📖 Docs:          http://localhost:9000/docs"
    echo ""
    echo "Pour arrêter: kill $API_PID"
    echo ""
    
    # Garder le processus actif
    wait $API_PID
}

# Menu principal
main() {
    check_requirements
    install_apktool
    install_apksigner
    install_python_deps
    setup_project
    
    echo ""
    echo -e "${GREEN}✓ Installation terminée avec succès!${NC}"
    echo ""
    
    read -p "Voulez-vous démarrer Mobile-Morpher maintenant? (O/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Oo]$ ]] || [[ -z $REPLY ]]; then
        start_app
    else
        echo ""
        echo "Pour démarrer manuellement:"
        echo "  cd $(pwd)"
        echo "  source venv/bin/activate"
        echo "  uvicorn main:app --host 0.0.0.0 --port 9000"
    fi
}

# Exécution
main "$@"