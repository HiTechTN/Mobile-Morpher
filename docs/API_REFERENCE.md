# API Reference - Mobile-Morpher

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Upload APK
Télécharge un fichier APK pour traitement.

**Endpoint:** `POST /api/upload`

**Content-Type:** `multipart/form-data`

**Request:**
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@application.apk"
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "uploaded"
}
```

---

### 2. Process APK
Lance le traitement de l'APK avec les paramètres spécifiés.

**Endpoint:** `POST /api/process/{session_id}`

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "new_app_name": "MonApp Pro",
  "new_package_id": "com.monentreprise.monapp",
  "mode": "express",
  "ai_suggestions": []
}
```

**Modes disponibles:**
- `express`: Transformation rapide (120s)
- `design`: Personnalisation esthétique
- `developer`: Accès complet au code

**Response:**
```json
{
  "status": "success",
  "output_path": "/app/shared-volume/{session_id}/modified.apk",
  "refactor_details": {
    "manifest_updated": 1,
    "smali_updated": 15,
    "resources_updated": 3,
    "directories_renamed": 1,
    "errors": []
  },
  "suggestions": [
    {
      "type": "ads",
      "message": "Publicité détectée dans MainActivity.smali",
      "file": "smali/com/original/app/MainActivity.smali",
      "action": "remove_ads"
    }
  ]
}
```

---

### 3. Download APK
Télécharge l'APK modifié.

**Endpoint:** `GET /api/download/{session_id}`

**Response:** Fichier APK (binary)

**Example:**
```bash
curl -O http://localhost:8000/api/download/550e8400-e29b-41d4-a716-446655440000
```

---

### 4. Cleanup Session
Supprime les fichiers temporaires d'une session.

**Endpoint:** `DELETE /api/cleanup/{session_id}`

**Response:**
```json
{
  "status": "cleaned"
}
```

---

## Codes d'erreur

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Paramètres invalides |
| 404 | Not Found | Session ou fichier non trouvé |
| 500 | Internal Server Error | Erreur lors du traitement |

## Exemple d'utilisation complète

```bash
# 1. Upload
SESSION_ID=$(curl -s -X POST http://localhost:8000/api/upload \
  -F "file=@app.apk" | jq -r '.session_id')

# 2. Process
curl -X POST http://localhost:8000/api/process/$SESSION_ID \
  -H "Content-Type: application/json" \
  -d '{
    "new_app_name": "My Custom App",
    "new_package_id": "com.custom.app",
    "mode": "express"
  }'

# 3. Download
curl -O http://localhost:8000/api/download/$SESSION_ID

# 4. Cleanup
curl -X DELETE http://localhost:8000/api/cleanup/$SESSION_ID
```
