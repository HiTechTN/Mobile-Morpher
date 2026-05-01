# Scénarios Vidéos - Mobile-Morpher

## 📹 VIDÉO 1: Installation (5 min)

### 00:00 - Introduction (30s)
- Titre: "Installer Mobile-Morpher en 3 minutes"
- Présenter l'outil: transformation d'APK Android

### 00:30 - Prérequis (1min)
- Docker et Docker Compose installés
- Commande: `docker --version`
- Commande: `docker compose version`

### 01:30 - Clonage du projet (1min)
```
git clone https://github.com/HiTechTN/Mobile-Morpher.git
cd Mobile-Morpher
```

### 02:30 - Configuration (1min)
- Ouvrir docker-compose.yml
- Expliquer les ports: 9000 (API), 9001 (Web)

### 03:30 - Résumé (30s)
- "Dans la prochaine vidéo, nous lançons le projet"

---

## 📹 VIDÉO 2: Lancement (3 min)

### 00:00 - Introduction (30s)
- Rappel: projet cloné
- Objectif: faire tourner les conteneurs

### 00:30 - Lancement Docker (1min)
```
docker compose up -d --build
```
- Expliquer les étapes de build
- Patience pendant le téléchargement des images

### 01:30 - Vérification (1min)
```
docker ps
```
- Montrer: mobile-morpher-api sur port 9000
- Montrer: mobile-morpher-web sur port 9001

### 02:30 - Accès aux interfaces (30s)
- http://localhost:9001 → Interface Web
- http://localhost:9000/docs → API Swagger

---

## 📹 VIDÉO 3: Utilisation (7 min)

### 00:00 - Introduction (30s)
- Présenter les 3 modes: Express, Design, Developer

### 00:30 - Interface Web (1min)
- Visite de la page d'accueil
- Présentation des zones: mode selector, upload, config

### 01:30 - Préparation APK (1min)
- Télécharger un APK test
- Conseils: APK non protégé, pas de Schutz

### 02:30 - Upload et Configuration (2min)
- Sélectionner le fichier APK
- Choisir le mode (Express)
- Remplir: Nom de l'app, Package ID
- Bouton "Transformer l'APK"

### 04:30 - Traitement (1min)
- Attendre la barre de progression
- Expliquer: décompilation → modification → recompilation → signature

### 05:30 - Téléchargement (1min)
- Bouton de téléchargement verts
- Vérifier que l'APK fonctionne

### 06:30 - Conclusion (30s)
- Récapitulatif
- Conseils pour aller plus loin

---

## 🎬 Checklist Technique

### Avant l'enregistrement:
- [ ] Fond d'écran nettoyé
- [ ] Fenêtres inutiles fermées
- [ ] Terminal prêt avec commandes
- [ ] Navigateur ouvert sur http://localhost:9001

### Pendant l'enregistrement:
- [ ] Micro activé et测试
- [ ] Luminosité écran适当
- [ ] Cursor visible

### Post-production:
- [ ] Réduire les silences
- [ ] Ajouter sous-titres
- [ ] Ajouter musique douce (optionnel)