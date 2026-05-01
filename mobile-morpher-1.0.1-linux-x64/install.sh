#!/bin/bash

echo "Mobile-Morpher - Installation Linux/macOS"
echo "========================================"

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé. Installation..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt update && sudo apt install -y docker.io docker-compose-v2
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Veuillez installer Docker Desktop pour Mac"
        exit 1
    fi
fi

# Cloner le projet
if [ ! -d "Mobile-Morpher" ]; then
    git clone https://github.com/HiTechTN/Mobile-Morpher.git
    cd Mobile-Morpher
else
    cd Mobile-Morpher
    git pull
fi

# Lancer avec Docker Compose
echo "Lancement des services..."
docker compose up -d

echo ""
echo "✓ Installation terminée!"
echo "✓ Interface Web: http://localhost:9001"
echo "✓ API Docs: http://localhost:9000/docs"
