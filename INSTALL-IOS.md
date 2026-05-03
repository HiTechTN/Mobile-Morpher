# Installation iOS (via iSH)

## Prérequis
1. Installer **iSH** depuis l'[App Store](https://apps.apple.com/app/ish-shell/id1436902243)

## Installation
```bash
# 1. Mettre à jour les paquets
apk update && apk upgrade

# 2. Installer les outils
apk add git docker docker-compose

# 3. Télécharger et lancer
curl -fsSL https://github.com/HiTechTN/Mobile-Morpher/releases/download/v1.0.0/install.sh | bash

# 4. Accéder dans Safari
# http://localhost:9001
```

## Limites connues
- iSH est une émulation x86 sur iOS, donc les performances sont limitées
- Docker peut être difficile à faire fonctionner sur iSH
- Pour une meilleure expérience, utilisez un serveur distant
