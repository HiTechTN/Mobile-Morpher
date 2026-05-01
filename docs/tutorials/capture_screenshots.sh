#!/bin/bash

OUTPUT_DIR="docs/tutorials/screenshots"
mkdir -p "$OUTPUT_DIR"

echo "=== Capture d'écran Mobile-Morpher ==="

capture_screenshot() {
    local name=$1
    local url=$2
    
    echo "Capture: $name"
    # Utiliser chromium headless pour capturer
    if command -v chromium &> /dev/null; then
        chromium --headless --disable-gpu \
            --screenshot="$OUTPUT_DIR/$name.png" \
            --window-size=1920,1080 \
            --virtual-time-budget=5000 \
            "$url" 2>/dev/null
        echo "  -> $OUTPUT_DIR/$name.png"
    elif command -v firefox &> /dev/null; then
        echo "Firefox détecté, utilisation alternative..."
        # Alternative avec wkhtmltopdf ou autre
        echo "Installation de chromium recommandée pour captures automatiques"
    fi
}

# Captures principales
capture_screenshot "01-homepage" "http://localhost:9001"
capture_screenshot "02-apidocs" "http://localhost:9000/docs"

echo ""
echo "Captures terminées!"
ls -la "$OUTPUT_DIR/"