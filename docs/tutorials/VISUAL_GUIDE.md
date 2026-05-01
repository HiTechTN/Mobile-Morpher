# Guide Visuel - Mobile-Morpher

## 🚀 Accès aux Interfaces

| Service | URL | Description |
|---------|-----|-------------|
| Interface Web | http://localhost:9001 | Application principale |
| API Docs | http://localhost:9000/docs | Documentation Swagger |

---

## 📱 Interface Web - Page d'Accueil

### 1. Header
- Logo/Motif de fond
- Titre: "Mobile-Morpher"
- Sous-titre: "Transformez vos applications Android"

### 2. Zone Mode de Transformation
3 cartes cliquables:
- ⚡ **Express** - Transformation rapide (120s)
- 🎨 **Design** - Personnalisation complète
- 🔧 **Developer** - Accès complet Smali

### 3. Zone Upload APK
Zone de drag & drop avec:
- Icône de téléchargement
- Texte: "Glissez votre fichier APK ici"
- Bouton parcourir

### 4. Zone Configuration
Deux champs:
- "Nom de l'application" → ex: "MonApp"
- "Package ID" → ex: "com.monapp.pro"

### 5. Bouton Principal
- "Transformer l'APK" avec icône молнии

### 6. États
- Loading: Spinner + "Traitement en cours..."
- Succès: Bouton télécharger vert
- Erreur: Message rouge

---

## 🔧 Interface API (Swagger)

### Endpoints Principaux

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/upload | Upload APK |
| POST | /api/process/{session_id} | Traite transformation |
| GET | /api/download/{session_id} | Télécharge APK résultat |
| DELETE | /api/cleanup/{session_id} | Nettoie session |

---

## 💻 Workflow Terminal

```bash
# 1. Lancer les services
docker compose up -d

# 2. Vérifier l'état
docker ps

# 3. Voir les logs
docker compose logs -f

# 4. Arrêter
docker compose down
```

---

## 📦 Structure du Projet

```
Mobile-Morpher/
├── docker-compose.yml      # Orchestration
├── web-ui/                 # Interface Next.js
│   ├── pages/index.js     # Page principale
│   └── styles/            # CSS Tailwind
├── api-service/           # Backend FastAPI
│   ├── main.py           # API principale
│   ├── core/             # Traitement APK
│   ├── morpher/          # Refactoring
│   └── ai_engine/        # Analyse IA
└── shared-volume/         # Stockage temporaire
```

---

## 🔍 Dépannage

| Problème | Solution |
|---------|----------|
| Port 9000 occupé | Vérifier avec `lsof -i :9000` |
| Container échoue | `docker compose logs api-service` |
| APK non valide | Utiliser APK non protégé |
| Timeout | Mode Express plus rapide |