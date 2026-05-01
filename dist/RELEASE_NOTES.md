# Mobile-Morpher v1.0.1 - Release Notes

## 📦 Téléchargements

### Code Source
- [mobile-morpher-1.0.1-source.tar.gz](./mobile-morpher-1.0.1-source.tar.gz) - Code source complet

### Docker (Recommandé)
```bash
docker pull hitechtn/mobile-morpher:latest
docker run -p 9000:9000 -p 9001:9001 hitechtn/mobile-morpher
```

## 🚀 Installation Rapide

### Avec Docker (Recommandé)
```bash
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
docker compose up -d
# Web: http://localhost:9001
# API: http://localhost:9000
```

### Sans Docker (Linux)
```bash
chmod +x install-native.sh
./install-native.sh
```

### Sans Docker (Windows)
1. Installez Python 3.10+ et Java JDK 17
2. Exécutez `install-native.bat`

## ✨ Nouvelles Fonctionnalités

1. **Interface Web Modernisée** - Design sombre élégant
2. **Zone Drag & Drop** - Upload APK simplifié
3. **Validation Package ID** - Vérification en temps réel
4. **Barre de Progression** - Feedback visuel
5. **Tutoriels Vidéo** - Guide complet
6. **Builds Nats** - Linux, Windows, macOS sans Docker

## 🐛 Corrections

- Correction du chemin de décompilation pour le refactoring APK
- Meilleure gestion des erreurs

## 🌍 Compatibilité

| Platform | Docker | Native |
|----------|--------|--------|
| Linux | ✅ | ✅ |
| Windows | ✅ | ✅ |
| macOS | ✅ | ✅ |
| Android | 🔜 | - |
