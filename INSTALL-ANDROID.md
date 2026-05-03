# Installation Android (via Termux)

## Prérequis
1. Installer **Termux** depuis [F-Droid](https://f-droid.org/packages/com.termux/) (pas Google Play)
2. Installer **Docker** dans Termux

## Installation
```bash
# 1. Mettre à jour Termux
pkg update && pkg upgrade

# 2. Installer les outils nécessaires
pkg install git docker docker-compose

# 3. Télécharger et lancer
curl -fsSL https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/install.sh | bash

# 4. Accéder dans votre navigateur
# http://localhost:9001
```

## Note
- Assurez-vous que le port 9001 n'est pas bloqué par le pare-feu Android
- L'interface est responsive et fonctionne bien sur mobile
