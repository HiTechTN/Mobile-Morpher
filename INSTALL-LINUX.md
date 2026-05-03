# Installation Linux

## Méthode 1 : Script automatique (Recommandé)
```bash
curl -fsSL https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/install.sh | bash
```

## Méthode 2 : Manuelle
```bash
# 1. Télécharger et extraire
wget https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/mobile-morpher-v1.0.0-linux.tar.gz
tar -xzf mobile-morpher-v1.0.0-linux.tar.gz
cd Mobile-Morpher

# 2. Installer Docker si nécessaire
sudo apt update && sudo apt install -y docker.io docker-compose-v2

# 3. Lancer
docker compose up -d

# 4. Accéder
# Interface: http://localhost:9001
# API: http://localhost:9000/docs
```

## Méthode 3 : Docker direct
```bash
docker run -d -p 9000:8000 -p 9001:3000 \
  --name mobile-morpher \
  ghcr.io/hitechn/obile-morpher/api-service:v1.0.0
```
