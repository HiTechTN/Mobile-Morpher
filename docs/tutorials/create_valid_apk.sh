#!/bin/bash
# Créer un APK de test valide pour apktool

set -e

WORK_DIR="/tmp/valid_apk"
mkdir -p "$WORK_DIR"

echo "=== Création APK valide ==="

# Structure minimale Android
mkdir -p "$WORK_DIR/res/values"
mkdir -p "$WORK_DIR/res/drawable"
mkdir -p "$WORK_DIR/smali/com/test/app"

# AndroidManifest.xml (format valide)
cat > "$WORK_DIR/AndroidManifest.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.test.app">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="34"/>

    <uses-permission android:name="android.permission.INTERNET"/>

    <application
        android:label="@string/app_name"
        android:icon="@drawable/icon"
        android:allowBackup="true">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

    </application>

</manifest>
EOF

# strings.xml
cat > "$WORK_DIR/res/values/strings.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">TestApp</string>
</resources>
EOF

# Couleurs
cat > "$WORK_DIR/res/values/colors.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="purple_200">#FFBB86FC</color>
    <color name="purple_500">#FF6200EE</color>
    <color name="purple_700">#FF3700B3</color>
    <color name="teal_200">#FF03DAC5</color>
    <color name="teal_700">#FF018786</color>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
</resources>
EOF

# Thème
cat > "$WORK_DIR/res/values/themes.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.TestApp" parent="android:Theme.Material.Light.NoActionBar"/>
</resources>
EOF

# Icone simple (1x1 pixel PNG transparent)
echo -e '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82' > "$WORK_DIR/res/drawable/icon.png"

# Code Smali minimal
cat > "$WORK_DIR/smali/com/test/app/MainActivity.smali" << 'EOF'
.class public Lcom/test/app/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"

.method public constructor <init>()V
    .registers 1
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V
    return-void
.end method

.method protected onCreate(Landroid/os/Bundle;)V
    .registers 2
    invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V
    const v0, 0x7f0a0000
    invoke-virtual {p0, v0}, Lcom/test/app/MainActivity;->setContentView(I)V
    return-void
.end method
EOF

# public.xml pour les ressources
mkdir -p "$WORK_DIR/res/values/public"
cat > "$WORK_DIR/res/values/public.xml" << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <public type="layout" name="main" />
    <public type="string" name="app_name" id="0x7f0a0000" />
</resources>
EOF

# Build
OUTPUT="/tmp/testapp_valid.apk"
cd "$WORK_DIR"

echo "Décompilation..."
apktool d -f original.apk -o decompiled 2>/dev/null || true

echo "Exécution apktool..."
if apktool b "$WORK_DIR" -o "$OUTPUT" 2>&1; then
    echo "APK compilé: $OUTPUT"
else
    echo "Erreur, tentative alternative..."
    # Créer manuellement le APK
    zip -r "$OUTPUT" . 2>/dev/null
fi

ls -la "$OUTPUT"

echo "=== Terminé ==="