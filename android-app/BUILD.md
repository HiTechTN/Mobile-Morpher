# Mobile-Morpher Android App - Build Instructions

## Option 1: Build with Android Studio

1. **Télécharger Android Studio**
   - https://developer.android.com/studio

2. **Ouvrir le projet**
   - Ouvrir le dossier `android-app` dans Android Studio

3. **Build APK**
   - Menu: Build → Build Bundle(s) / APK(s) → Build APK(s)
   - L'APK sera généré dans `app/build/outputs/apk/debug/`

## Option 2: Build en ligne de commande

```bash
# Installer Gradle
sdk install gradle 8.4

# Dans le dossier android-app
cd android-app

# Générer le projet Gradle
gradle wrapper

# Compiler
./gradlew assembleDebug
```

## Option 3: Build avec GitHub Actions (Automatique)

Le projet inclut `.github/workflows/android.yml` qui compile automatiquement l'APK à chaque push.

## Fichier généré

L'APK final: `android-app/app/build/outputs/apk/debug/app-debug.apk`

## Installation sur Android

1. Transférer l'APK sur votre téléphone
2. Activer "Sources inconnues" dans les paramètres
3. Installer l'APK
4. L'app se connectera à votre serveur Mobile-Morpher

## Configuration

Pour changer l'API URL, modifiez:
- `api/ApiService.kt` - Modifier `BASE_URL`

Par défaut, l'app utilise `http://10.0.2.2:9000` (localhost de l'émulateur Android)