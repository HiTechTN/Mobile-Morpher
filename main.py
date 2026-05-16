from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import shutil
import os
import uuid
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "api-service"))

from morpher.refactor import refactor_apk
from ai_engine.analyzer import AIAnalyzer
from ai_engine.applier import apply_suggestions
from core.apk_processor import APKProcessor

app = FastAPI(title="Mobile-Morpher", version="1.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:9000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

WORK_DIR = Path(os.environ.get("WORK_DIR", "/tmp/mobile-morpher"))
WORK_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATE_PATH = Path(__file__).parent / "web-ui" / "templates" / "index.html"
HTML_TEMPLATE = TEMPLATE_PATH.read_text(encoding="utf-8") if TEMPLATE_PATH.exists() else "<h1>Mobile-Morpher</h1>"


class RefactorConfig(BaseModel):
    new_app_name: str
    new_package_id: str
    mode: str = "express"
    ai_suggestions: Optional[List[str]] = []


def apply_modern_theme(decompiled_dir: str):
    try:
        colors_path = Path(decompiled_dir) / "res" / "values" / "colors.xml"
        if colors_path.exists():
            content = colors_path.read_text()
            if "colorPrimary" not in content:
                colors_content = content.replace("</resources>",
                    """    <color name="colorPrimary">#6750A4</color>
    <color name="colorPrimaryDark">#4F378B</color>
    <color name="colorAccent">#625B71</color>
</resources>""")
                colors_path.write_text(colors_content)
    except Exception:
        pass


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE


@app.post("/api/upload")
async def upload_apk(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    session_dir = WORK_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    apk_path = session_dir / "original.apk"
    with open(apk_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"session_id": session_id, "status": "uploaded"}


@app.post("/api/process/{session_id}")
async def process_apk(session_id: str, config: RefactorConfig):
    session_dir = WORK_DIR / session_id
    if not session_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")

    processor = APKProcessor(session_dir)

    try:
        processor.decompile()
        old_package = processor.get_package_name()
        old_app_name = processor.get_app_name()

        decompiled_dir = session_dir / "decompiled"
        refactor_results = refactor_apk(
            str(decompiled_dir),
            old_package,
            config.new_package_id,
            old_app_name,
            config.new_app_name,
        )

        suggestions = []
        applier_results = {}

        if config.mode == "design":
            analyzer = AIAnalyzer(decompiled_dir)
            suggestions = analyzer.analyze()
            apply_modern_theme(str(decompiled_dir))

        elif config.mode == "developer":
            analyzer = AIAnalyzer(decompiled_dir)
            suggestions = analyzer.analyze()

        if suggestions:
            applier_results = apply_suggestions(str(decompiled_dir), suggestions)

        processor.rebuild()
        processor.sign(config.new_package_id)

        return {
            "status": "success",
            "session_id": session_id,
            "mode": config.mode,
            "old_package": old_package,
            "new_package": config.new_package_id,
            "refactor_details": refactor_results,
            "suggestions": suggestions,
            "applied": applier_results,
        }

    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=400,
            detail=f"APK invalide ou corrompu: {e.stderr or e.stdout}"
        )
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"{e}\n{traceback.format_exc()}")


@app.get("/api/download/{session_id}")
async def download_apk(session_id: str):
    output_path = WORK_DIR / session_id / "modified.apk"
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="APK not found")
    return FileResponse(
        str(output_path),
        media_type="application/vnd.android.package-archive",
        filename="modified.apk",
    )


@app.delete("/api/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    session_dir = WORK_DIR / session_id
    if session_dir.exists():
        shutil.rmtree(session_dir)
    return {"status": "cleaned"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
