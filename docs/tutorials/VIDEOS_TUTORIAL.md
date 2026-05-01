# Tutoriels Vidéo Mobile-Morpher

## 📹 Liste des Tutoriels

### Vidéo 1: Installation
- Durée estimée: 3-5 minutes
- Contenu: Prérequis, clonage, configuration Docker

### Vidéo 2: Lancement
- Durée estimée: 2-3 minutes
- Contenu: Démarrage des conteneurs, vérification des services

### Vidéo 3: Utilisation
- Durée estimée: 5-7 minutes
- Contenu: Interface web, upload APK, transformation, téléchargement

---

## 🎬 Scripts d'Enregistrement

### Enregistrer avec FFmpeg

```bash
# Capture écran complet (pour Ubuntu/Linux)
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 \
  -i :0.0 -c:v libx264 -preset fast output.mp4

# Capture région spécifique
ffmpeg -f x11grab -framerate 30 -video_size 1280x720 \
  -i :0.0+100,50 -c:v libx264 output.mp4
```

---

## 📸 Captures d'Écran Automatisées

### Script de capture (save_screenshots.sh)

```bash
#!/bin/bash

# Capturer l'interface web
URL="http://localhost:9001"
OUTPUT_DIR="docs/tutorials/screenshots"

mkdir -p "$OUTPUT_DIR"

# Capture via Chromium headless
chromium --headless --disable-gpu \
  --screenshot="$OUTPUT_DIR/homepage.png" \
  --window-size=1920,1080 "$URL"

echo "Captures enregistrées dans $OUTPUT_DIR"
```

---

## 🔧 Méthode Alternative: asciinema (Terminal)

Pour les parties terminal/installation:

```bash
# Installer asciinema
pip install asciinema

# Enregistrer une session terminal
asciinema rec install.cast

# Plus tard: ajouter à la doc
asciinema upload install.cast
```

---

## 📋 Checklist Vidéo

### Pré-production
- [x] Structure du projet comprise
- [x] Scripts de démonstration prêts
- [ ] APK de test valide préparé

### Recording
- [ ] Installation (clone, docker)
- [ ] Lancement (docker compose up)
- [ ] Vérification (ports 9000, 9001)
- [ ] Interface web (capture d'écran)
- [ ] Upload APK (démo)
- [ ] Transformation (démo)

### Post-production
- [ ] Montage
- [ ] Titres et annotations
- [ ] Export final

---

## 🎥 Instructions pour Créer les Vidéos

### Équipement recommandé
- Enregistreur d'écran: OBS, Kazam, ou FFmpeg
- Microphone: intégré ou externe
- Logiciel de montage: Kdenlive, Blender, ou Shotcut

### Structure recommandée par vidéo

**Vidéo 1 - Installation:**
1. Introduction (30s)
2. Prérequis Docker (1min)
3. Clone du projet (1min)
4. Configuration (1min)

**Vidéo 2 - Lancement:**
1. Rappel rapide (30s)
2. Docker Compose up (1min)
3. Vérification services (1min)
4. Accès interface (30s)

**Vidéo 3 - Utilisation:**
1. Présentation interface (1min)
2. Upload APK (2min)
3. Configuration transformation (2min)
4. Résultat téléchargement (1min)
5. Conclusion (30s)

---

## 🔗 Ressources Externes

- [OBS Project](https://obsproject.com) - Logiciel gratuit d'enregistrement
- [Kdenlive](https://kdenlive.org) - Montage vidéo gratuit
- [asciinema.org](https://asciinema.org) - Enregistrement terminal