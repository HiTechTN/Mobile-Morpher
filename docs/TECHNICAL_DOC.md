# Documentation Technique - Mobile-Morpher

## Architecture

### Vue d'ensemble
Mobile-Morpher utilise une architecture Dockerisée avec séparation frontend/backend.

```
┌─────────────────┐     HTTP/REST     ┌──────────────────┐
│   Web UI        │ ←──────────────→ │   API Service    │
│   (Next.js)     │                   │   (FastAPI)      │
│   Port: 3000    │                   │   Port: 8000     │
└─────────────────┘                   └──────────────────┘
         │                                      │
         └────────── Docker Network ────────────┘
                          │
                          ▼
                ┌──────────────────┐
                │ Shared Volume    │
                │ (APK temporaire) │
                └──────────────────┘
```

### Backend (FastAPI)

#### Modules principaux
- **main.py**: Points d'entrée API REST
- **core/apk_processor.py**: Gestion Apktool, décompilation, compilation, signature
- **morpher/refactor.py**: Renommage intelligent du package et de l'app
- **ai_engine/analyzer.py**: Analyse de code et suggestions

#### API Endpoints
- `POST /api/upload`: Upload de l'APK
- `POST /api/process/{session_id}`: Traitement avec configuration
- `GET /api/download/{session_id}`: Téléchargement de l'APK modifié
- `DELETE /api/cleanup/{session_id}`: Nettoyage de session

### Frontend (Next.js)

#### Structure
```
web-ui/
├── pages/
│   ├── index.js         # Interface principale
│   └── _app.js          # Configuration App
├── styles/
│   └── globals.css      # Styles globaux
└── package.json
```

#### Modes d'interface
- **Express**: Formulaire minimaliste
- **Design**: Options d'esthétique
- **Developer**: Éditeur de code intégré

## Outils utilisés

### Apktool (v2.9.3)
Décompilation et recompilation des APK.
```bash
apktool d app.apk -o output/
apktool b input/ -o output.apk
```

### Uber APK Signer
Signature des APK avec clés V2/V3.
```bash
apksigner sign --ks keystore.jks app.apk
```

### Luyten
Prévisualisation Java (optionnel, via interface web).

## Workflow de transformation

1. **Upload**: L'APK est stocké dans `/shared-volume/{session_id}/`
2. **Décompilation**: Apktool extrait les ressources et le code Smali
3. **Analyse**: Lecture du `AndroidManifest.xml` pour extraire le package et le nom
4. **Refactoring**:
   - Remplacement du nom de package dans tous les fichiers
   - Renommage des répertoires Smali
   - Mise à jour du manifest et des ressources
5. **IA (optionnel)**: Analyse du code pour suggestions
6. **Recompilation**: Apktool reconstruit l'APK
7. **Signature**: Génération d'une clé unique et signature V2/V3
8. **Téléchargement**: L'utilisateur récupère l'APK modifié
9. **Nettoyage**: Suppression des fichiers temporaires

## Sécurité

- Aucune persistance des APK après téléchargement
- Clés de signature uniques par session
- Isolation via conteneurs Docker
- Nettoyage automatique du volume partagé

## Configuration

Variables d'environnement (fichier `.env`):
```env
API_PORT=8000
WEB_PORT=3000
WORK_DIR=/app/shared-volume
AI_PROVIDER=ollama
AI_MODEL=codellama
```

## Tests

```bash
# Tests backend
docker exec -it mobile-morpher-api pytest

# Tests frontend
docker exec -it mobile-morpher-web npm test
```

## Dépannage

**Erreur: "Apktool not found"**
→ Vérifiez que l'image Docker est bien construite : `docker-compose build`

**Erreur: "Permission denied"**
→ Vérifiez les permissions du volume partagé : `chmod 777 shared-volume/`

**L'APK modifié ne s'installe pas**
→ Vérifiez les logs : `docker logs mobile-morpher-api`
