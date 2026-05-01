#!/bin/bash

# Script d'enregistrement vidéo pour Mobile-Morpher
# Utilisation: ./record_video.sh [output_file.mp4]

OUTPUT_FILE="${1:-tutoriel_mobile_morpher.mp4}"
FRAMERATE=30
VIDEO_SIZE="1920x1080"

echo "=== Enregistreur Vidéo Mobile-Morpher ==="
echo "Appuyez sur Ctrl+C pour arrêter l'enregistrement"
echo ""

# Vérifier ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "ERREUR: ffmpeg n'est pas installé"
    echo "Installez-le avec: apt install ffmpeg"
    exit 1
fi

# Vérifier si on est dans un environnement graphique
if [ -z "$DISPLAY" ]; then
    echo "ERREUR: Pas d'affichage détecté (DISPLAY non défini)"
    echo "Utilisation avec X11 requise"
    exit 1
fi

echo "Démarrage de l'enregistrement..."
echo "Fichier de sortie: $OUTPUT_FILE"
echo "Appuyez sur q pour arrêter"

# Enregistrement avec prévisualisation
ffmpeg -f x11grab -framerate $FRAMERATE \
    -video_size $VIDEO_SIZE \
    -i :0.0 \
    -c:v libx264 -preset fast \
    -crf 23 \
    -pix_fmt yuv420p \
    "$OUTPUT_FILE"

echo ""
echo "Enregistrement terminé: $OUTPUT_FILE"