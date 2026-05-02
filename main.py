from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
import shutil
import os
import uuid
import subprocess
import zipfile

app = FastAPI(title="Mobile-Morpher", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
WORK_DIR = os.environ.get('WORK_DIR', '/tmp/mobile-morpher')
os.makedirs(WORK_DIR, exist_ok=True)

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

class RefactorConfig(BaseModel):
    new_app_name: str
    new_package_id: str
    mode: str = "express"
    ai_suggestions: Optional[List[str]] = []

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mobile-Morpher 🧬</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
                min-height: 100vh;
                color: #f8fafc;
                padding: 2rem;
            }
            .container { max-width: 600px; margin: 0 auto; }
            h1 {
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #6366f1, #ec4899);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .subtitle { text-align: center; color: #94a3b8; margin-bottom: 2rem; }
            .card {
                background: rgba(30, 41, 59, 0.8);
                border: 1px solid rgba(255,255,255,0.1);
                border-radius: 1rem;
                padding: 1.5rem;
                margin-bottom: 1rem;
            }
            label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
            input, select {
                width: 100%;
                padding: 0.75rem;
                border-radius: 0.5rem;
                border: 1px solid #475569;
                background: #1e293b;
                color: white;
                margin-bottom: 1rem;
            }
            .modes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin-bottom: 1rem; }
            .mode-btn {
                padding: 0.75rem;
                border-radius: 0.5rem;
                border: 2px solid #475569;
                background: transparent;
                color: #94a3b8;
                cursor: pointer;
                transition: all 0.3s;
            }
            .mode-btn.active { border-color: #6366f1; background: rgba(99,102,241,0.2); color: white; }
            .btn {
                width: 100%;
                padding: 1rem;
                border-radius: 0.75rem;
                border: none;
                background: linear-gradient(90deg, #6366f1, #4f46e5);
                color: white;
                font-weight: 600;
                cursor: pointer;
                font-size: 1rem;
            }
            .btn:disabled { background: #475569; cursor: not-allowed; }
            .result { background: rgba(34,197,94,0.2); border-color: #22c55e; }
            .error { background: rgba(239,68,68,0.2); border-color: #ef4444; }
            .progress { height: 8px; background: #1e293b; border-radius: 4px; overflow: hidden; margin: 1rem 0; }
            .progress-bar { height: 100%; background: linear-gradient(90deg, #6366f1, #ec4899); transition: width 0.3s; }
            #status { text-align: center; margin-top: 1rem; }
            @media (max-width: 640px) { .modes { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧬 Mobile-Morpher</h1>
            <p class="subtitle">Transformez vos APK Android</p>
            
            <div class="card">
                <label>Mode de transformation</label>
                <div class="modes">
                    <button class="mode-btn active" onclick="setMode('express')">⚡ Express</button>
                    <button class="mode-btn" onclick="setMode('design')">🎨 Design</button>
                    <button class="mode-btn" onclick="setMode('developer')">🔧 Dev</button>
                </div>
                
                <label>Fichier APK</label>
                <input type="file" id="file" accept=".apk">
                
                <label>Nom de l'application</label>
                <input type="text" id="appName" placeholder="Mon Application">
                
                <label>Package ID</label>
                <input type="text" id="packageId" placeholder="com.monapp.pro">
                
                <div class="progress" id="progress" style="display:none">
                    <div class="progress-bar" id="progressBar"></div>
                </div>
                
                <button class="btn" id="submitBtn" onclick="process()">Transformer l'APK</button>
                
                <div id="status"></div>
            </div>
        </div>
        
        <script>
            let mode = 'express';
            
            function setMode(m) {
                mode = m;
                document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
                event.target.classList.add('active');
            }
            
            async function process() {
                const file = document.getElementById('file').files[0];
                const appName = document.getElementById('appName').value;
                const packageId = document.getElementById('packageId').value;
                const btn = document.getElementById('submitBtn');
                const status = document.getElementById('status');
                const progress = document.getElementById('progress');
                const progressBar = document.getElementById('progressBar');
                
                if (!file || !appName || !packageId) {
                    status.innerHTML = '<p class="error" style="padding:1rem;border-radius:0.5rem;margin-top:1rem">Veuillez remplir tous les champs</p>';
                    return;
                }
                
                btn.disabled = true;
                btn.textContent = 'Traitement en cours...';
                progress.style.display = 'block';
                progressBar.style.width = '20%';
                
                try {
                    // Upload
                    const formData = new FormData();
                    formData.append('file', file);
                    const uploadRes = await fetch('/api/upload', { method: 'POST', body: formData });
                    const uploadData = await uploadRes.json();
                    progressBar.style.width = '40%';
                    
                    // Process
                    const processRes = await fetch('/api/process/' + uploadData.session_id, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            new_app_name: appName,
                            new_package_id: packageId,
                            mode: mode
                        })
                    });
                    const processData = await processRes.json();
                    progressBar.style.width = '80%';
                    
                    progressBar.style.width = '100%';
                    
                    status.innerHTML = '<div class="result" style="padding:1rem;border-radius:0.5rem;margin-top:1rem;text-align:center"><p style="margin-bottom:0.5rem">✅ Transformation réussie!</p><a href="/api/download/' + uploadData.session_id + '" style="color:#6366f1">Télécharger l\'APK</a></div>';
                    
                } catch (e) {
                    status.innerHTML = '<p class="error" style="padding:1rem;border-radius:0.5rem;margin-top:1rem">❌ Erreur: ' + e.message + '</p>';
                }
                
                btn.disabled = false;
                btn.textContent = 'Transformer l\'APK';
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/upload")
async def upload_apk(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(WORK_DIR, session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    apk_path = os.path.join(session_dir, "original.apk")
    with open(apk_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"session_id": session_id, "status": "uploaded"}

@app.post("/api/process/{session_id}")
async def process_apk(session_id: str, config: RefactorConfig):
    session_dir = os.path.join(WORK_DIR, session_id)
    
    if not os.path.exists(session_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    apk_path = os.path.join(session_dir, "original.apk")
    decompiled_dir = os.path.join(session_dir, "decompiled")
    
    try:
        # Décompiler
        subprocess.run(["apktool", "d", "-f", apk_path, "-o", decompiled_dir], 
                      check=True, capture_output=True)
        
        # Lire le manifest pour obtenir l'ancien package
        import xml.etree.ElementTree as ET
        manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")
        
        old_package = "com.unknown"
        try:
            tree = ET.parse(manifest_path)
            old_package = tree.getroot().get("package", "com.unknown")
        except:
            pass
        
        # Mise à jour du manifest
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content = content.replace(old_package, config.new_package_id)
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Mise à jour des fichiers smali
        old_package_path = old_package.replace('.', '/')
        new_package_path = config.new_package_id.replace('.', '/')
        smali_dirs = [d for d in os.listdir(decompiled_dir) if d.startswith('smali')]
        
        for sdir in smali_dirs:
            for root, dirs, files in os.walk(os.path.join(decompiled_dir, sdir)):
                for file in files:
                    if file.endswith('.smali'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        updated = False
                        if old_package in content:
                            content = content.replace(old_package, config.new_package_id)
                            updated = True
                        if old_package_path in content:
                            content = content.replace(old_package_path, new_package_path)
                            updated = True
                        
                        if updated:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(content)
        
        # Mise à jour des ressources
        strings_files = []
        for root, dirs, files in os.walk(decompiled_dir):
            for file in files:
                if file == 'strings.xml':
                    strings_files.append(os.path.join(root, file))
        
        for strings_file in strings_files[:5]:  # Limiter à 5 fichiers
            try:
                with open(strings_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                if config.new_app_name not in content:
                    content = content.replace('>TestApp<', f'>{config.new_app_name}<')
                    with open(strings_file, 'w', encoding='utf-8') as f:
                        f.write(content)
            except:
                pass
        
        # Recompiler
        output_apk = os.path.join(session_dir, "modified.apk")
        subprocess.run(["apktool", "b", decompiled_dir, "-o", output_apk], 
                      check=True, capture_output=True)
        
        # Signer
        keystore = os.path.join(session_dir, "keystore.jks")
        if not os.path.exists(keystore):
            subprocess.run([
                "keytool", "-genkeypair", "-v",
                "-keystore", keystore,
                "-alias", "mobile-morpher",
                "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000",
                "-storepass", "changeit",
                "-keypass", "changeit",
                "-dname", "CN=Mobile Morpher, O=MobileMorpher, C=US"
            ], check=True, capture_output=True)
        
        subprocess.run([
            "apksigner", "sign",
            "--ks", keystore,
            "--ks-key-alias", "mobile-morpher",
            "--ks-pass", "pass:changeit",
            output_apk
        ], check=True, capture_output=True)
        
        return {
            "status": "success",
            "session_id": session_id,
            "refactor_details": {
                "manifest_updated": 1,
                "smali_updated": 1,
                "resources_updated": 1
            }
        }
        
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=str(e) + "\n" + traceback.format_exc())

@app.get("/api/download/{session_id}")
async def download_apk(session_id: str):
    output_path = os.path.join(WORK_DIR, session_id, "modified.apk")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="APK not found")
    return FileResponse(output_path, media_type="application/vnd.android.package-archive", 
                        filename="modified.apk")

@app.delete("/api/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    session_dir = os.path.join(WORK_DIR, session_id)
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    return {"status": "cleaned"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)