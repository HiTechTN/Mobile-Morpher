from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path
import shutil
import os
import uuid

from core.apk_processor import APKProcessor
from morpher.refactor import refactor_apk
from ai_engine.analyzer import AIAnalyzer
from ai_engine.applier import apply_suggestions

app = FastAPI(title="Mobile-Morpher API", version="1.0.0")

ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:9000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Disposition"],
)

WORK_DIR = Path(os.environ.get("SHARED_VOLUME", "/app/shared-volume"))


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


@app.post("/api/upload")
async def upload_apk(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    work_dir = WORK_DIR / session_id
    work_dir.mkdir(parents=True, exist_ok=True)

    apk_path = work_dir / "original.apk"
    with open(apk_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"session_id": session_id, "status": "uploaded"}


@app.post("/api/process/{session_id}")
async def process_apk(session_id: str, config: RefactorConfig):
    work_dir = WORK_DIR / session_id
    if not work_dir.exists():
        raise HTTPException(status_code=404, detail="Session not found")

    processor = APKProcessor(work_dir)

    try:
        processor.decompile()
        old_package = processor.get_package_name()
        old_app_name = processor.get_app_name()

        decompiled_dir = work_dir / "decompiled"
        refactor_results = refactor_apk(
            str(decompiled_dir),
            old_package,
            config.new_package_id,
            old_app_name,
            config.new_app_name,
        )

        suggestions = []
        applier_results = {}

        if config.mode == "express":
            pass

        elif config.mode == "design":
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

    except Exception as e:
        error_msg = str(e)
        if "returned non-zero exit status" in error_msg:
            raise HTTPException(status_code=400, detail="APK invalide ou corrompu. Veuillez uploader un fichier APK valide.")
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)


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
    work_dir = WORK_DIR / session_id
    if work_dir.exists():
        shutil.rmtree(work_dir)
    return {"status": "cleaned"}
