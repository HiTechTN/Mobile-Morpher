# Mobile-Morpher 🧬

<div align="center">

[![Docker](https://img.shields.io/docker/image-size/hitechtn/mobile-morpher/latest?logo=docker)](https://hub.docker.com/r/hitechtn/mobile-morpher)
[![GitHub release](https://img.shields.io/github/v/release/HiTechTN/Mobile-Morpher?logo=github)](https://github.com/HiTechTN/Mobile-Morpher/releases)
[![License](https://img.shields.io/github/license/HiTechTN/Mobile-Morpher)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Docker-blue)](https://www.docker.com/)

**Transformez n'importe quel APK Android en une version personnalisée, optimisée et unique.**

[Site Web](https://morpher.hitechtn.com) · [Documentation](https://github.com/HiTechTN/Mobile-Morpher/wiki) · [Signaler un bug](https://github.com/HiTechTN/Mobile-Morpher/issues)

</div>

---

## ✨ Fonctionnalités

| Feature | Description |
|---------|-------------|
| 🎯 **Rename** | Changez le nom et le Package ID de n'importe quelle app |
| 🔄 **Rebrand** | Personnalisez icônes, couleurs et ressources |
| 🔐 **Signature** | Génération automatique de clés de signature uniques |
| ⚡ **Rapide** | Traitement en 2-3 minutes via API REST |
| 🔒 **Sécurisé** | Nettoyage automatique après chaque session |
| 🎨 **Design** | Personnalisation avancée des thèmes Material Design |

---

## 🚀 Démarrage Rapide

### Prérequis

- **Docker** et **Docker Compose** (v2+)
- **4 GB RAM** minimum
- **10 GB** espace disque

### Installation

```bash
# 1. Cloner le projet
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher

# 2. Lancer l'environnement
docker compose up -d --build

# 3. Accéder à l'application
# Interface Web: http://localhost:9001
# API Docs:      http://localhost:9000/docs
```

---

## 📱 Modes d'Utilisation

### ⚡ Mode Express
Transformation rapide (~2 min) : changement de nom et Package ID.

### 🎨 Mode Design  
Personnalisation complète : couleurs, polices, icônes, thèmes Material Design 3.

### 🔧 Mode Développeur
Accès complet au code Smali décompilé pour modifications avancées.

---

## 🖥️ Interface Web

![Interface](docs/screenshots/web-ui.png)

```
http://localhost:9001
```

### Utilisation

1. **Sélectionner** un fichier APK
2. **Choisir** le mode de transformation
3. **Configurer** : Nom de l'app + Package ID
4. **Transformez** et télécharghez le résultat

---

## 🔌 API REST

```bash
# Upload APK
curl -X POST http://localhost:9000/api/upload \
  -F "file=@app.apk"

# Transformer
curl -X POST http://localhost:9000/api/process/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"new_app_name": "MonApp", "new_package_id": "com.monapp.pro", "mode": "express"}'

# Télécharger
curl -O http://localhost:9000/shared-volume/{session_id}/modified.apk
```

Documentation interactive : http://localhost:9000/docs

---

## 🏗 Architecture

```
Mobile-Morpher/
├── docker-compose.yml       # Orchestration Docker
├── web-ui/                  # Frontend Next.js
│   └── pages/
│       └── index.js        # Interface utilisateur
├── api-service/             # Backend FastAPI
│   ├── main.py            # API REST
│   ├── core/              # Traitement APK (Apktool)
│   ├── morpher/           # Refactoring & Renaming
│   └── ai_engine/         # Analyse IA (optionnel)
├── shared-volume/          # Stockage temporaire
├── docs/                   # Documentation
│   ├── tutorials/        # Tutoriels vidéo
│   └── wiki/             # Wiki complet
└── INSTALL.md             # Guide multi-plateforme
```

---

## 📦 Téléchargements

| Platform | Status | Download |
|----------|--------|----------|
| 🐧 Linux | ✅ Disponible | [Docker](https://github.com/HiTechTN/Mobile-Morpher/releases) |
| 🪟 Windows | ✅ Disponible | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| 🍎 macOS | ✅ Disponible | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| 📱 Android | 🔜 Bientôt | Termux + Docker |

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. **Fork** le projet
2. Créer une **feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branch (`git push origin feature/AmazingFeature`)
5. Ouvrir une **Pull Request**

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

---

## 📝 License

Distribué sous licence **MIT**. Voir [LICENSE](LICENSE) pour plus d'informations.

---

## 📱 Application Android

### Application Native (Kotlin/Jetpack Compose)
Le code source est dans le dossier `android-app/`.

**Pour build l'APK:**
1. Ouvrir `android-app/` dans Android Studio
2. Build → Build APK
3. L'APK sera dans `app/build/outputs/apk/debug/`

### PWA (Application Web Progressif)
Accessible via le navigateur: **http://localhost:9001**

Peut être installée sur:
- 📱 Android (Chrome)
- 🍎 iOS (Safari)
- 💻 PC (Chrome/Edge)

### GitHub Actions
Le projet inclut un workflow automatique qui compile l'APK à chaque push:
- Fichier: `.github/workflows/android.yml`
- Artifacts disponibles dans les actions GitHub

---

## 🙏 Remerciements

- [Apktool](https://apktool.org/) - Pour le décompilage/recompilage APK
- [Apksigner](https://developer.android.com/studio/build/apksigner) - Pour la signature
- [FastAPI](https://fastapi.tiangolo.com/) - API backend
- [Next.js](https://nextjs.org/) - Interface utilisateur
- [Jetpack Compose](https://developer.android.com/compose) - UI Android

---

<div align="center">

Développé avec ❤️ par [HiTechTN](https://github.com/HiTechTN)

</div>