# Installation macOS

## Méthode 1 : Script automatique
```bash
curl -fsSL https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/install.sh | bash
```

## Méthode 2 : Manuelle
```bash
# 1. Installer Docker Desktop
# Télécharger depuis https://www.docker.com/products/docker-desktop/

# 2. Télécharger et extraire
curl -LO https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/mobile-morpher-v1.0.0-macos.tar.gz
tar -xzf mobile-morpher-v1.0.0-macos.tar.gz
cd Mobile-Morpher

# 3. Lancer
docker compose up -d

# 4. Accéder
# Interface: http://localhost:9001
```

## Pour Apple Silicon (M1/M2/M3)
Utiliser les images Docker multi-arch :
```bash
docker compose -f docker-compose.yml up -d
# Les images arm64 seront automatiquement téléchargées
```
