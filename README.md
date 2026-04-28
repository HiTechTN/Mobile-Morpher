# Mobile-Morpher

> Transformez n'importe quel APK en une version personnalisée, optimisée et unique.

## 🚀 Démarrage Rapide

### Prérequis
- Docker & Docker Compose
- 4 GB RAM minimum
- 10 GB espace disque

### Installation en 3 étapes

```bash
# 1. Cloner le projet
git clone https://github.com/votre-username/Mobile-Morpher.git
cd Mobile-Morpher

# 2. Lancer l'environnement
docker compose up -d

# 3. Accéder à l'application
# Interface Web: http://localhost:9001
# API Docs: http://localhost:9000/docs
```

## 📱 Modes d'Utilisation

### Mode Express
Transformation rapide en 120 secondes : changement de nom et d'icône.

### Mode Design
Personnalisation de l'esthétique : couleurs, polices, thèmes Material Design 3.

### Mode Développeur
Accès complet au code Smali, édition des classes et configuration avancée.

## 🏗 Architecture

```
Mobile-Morpher/
├── docker-compose.yml       # Orchestration multi-OS
├── web-ui/                  # Frontend PWA (Next.js)
├── api-service/             # Backend FastAPI
│   ├── core/               # Apktool & Signer
│   ├── morpher/            # Refactoring & Renaming
│   ├── ai-engine/          # Analyse IA
│   └── Dockerfile
└── shared-volume/          # Stockage temporaire sécurisé
```

## ⚙️ Configuration

### Variables d'environnement (.env)
```env
API_PORT=8000
WEB_PORT=3000
WORK_DIR=/app/shared-volume
AI_PROVIDER=ollama  # ou openai
AI_MODEL=codellama  # pour Ollama
```

## 🔒 Sécurité

- Aucun fichier conservé après la session
- Nettoyage automatique du volume partagé
- Clés de signature uniques par projet

## 📖 Documentation

- [Guide Utilisateur](docs/USER_GUIDE.md)
- [Documentation Technique](docs/TECHNICAL_DOC.md)
- [API Reference](docs/API_REFERENCE.md)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 Licence

MIT License - Voir [LICENSE](LICENSE)
