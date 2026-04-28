# Guide d'Installation Multi-Plateforme

## Windows

### Prérequis
- Docker Desktop pour Windows
- Git pour Windows

### Installation
```bash
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
```

Accéder à l'interface : http://localhost:9001

## macOS

### Prérequis
- Docker Desktop pour Mac
- Git (inclus avec Xcode Command Line Tools)

### Installation
```bash
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
```

Accéder à l'interface : http://localhost:9001

## Linux (Ubuntu/Debian)

### Prérequis
```bash
sudo apt update
sudo apt install docker.io docker-compose-v2 git
```

### Installation
```bash
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
```

Accéder à l'interface : http://localhost:9001

## Android (via Termux)

### Prérequis
Installer Termux depuis F-Droid (pas Google Play)

### Installation
```bash
pkg update && pkg install git docker docker-compose
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
```

Accéder à l'interface : http://localhost:9001

## iOS (via iSH)

### Prérequis
Installer iSH depuis l'App Store

### Installation
```bash
apk add git docker docker-compose
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
```

Accéder à l'interface via Safari : http://localhost:9001

## Vérification

L'interface devrait afficher "Mobile-Morpher" avec trois modes : Express, Design, Developer.
