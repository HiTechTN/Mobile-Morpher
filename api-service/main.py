from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import shutil
import os
import uuid

from core.apk_processor import APKProcessor
from morpher.refactor import refactor_apk
from ai_engine.analyzer import AIAnalyzer

app = FastAPI(title="Mobile-Morpher API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class RefactorConfig(BaseModel):
    new_app_name: str
    new_package_id: str
    mode: str = "express"
    ai_suggestions: Optional[List[str]] = []

@app.post("/api/upload")
async def upload_apk(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    work_dir = f"/app/shared-volume/{session_id}"
    os.makedirs(work_dir, exist_ok=True)
    
    apk_path = f"{work_dir}/original.apk"
    with open(apk_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"session_id": session_id, "status": "uploaded"}

@app.post("/api/process/{session_id}")
async def process_apk(session_id: str, config: RefactorConfig):
    work_dir = f"/app/shared-volume/{session_id}"
    
    if not os.path.exists(work_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    processor = APKProcessor(work_dir)
    
    try:
        processor.decompile()
        old_package = processor.get_package_name()
        old_app_name = processor.get_app_name()
        
        decompiled_dir = f"{work_dir}/decompiled"
        refactor_results = refactor_apk(
            decompiled_dir,
            old_package,
            config.new_package_id,
            old_app_name,
            config.new_app_name
        )
        
        if config.mode in ["design", "developer"]:
            analyzer = AIAnalyzer(work_dir)
            suggestions = analyzer.analyze()
        else:
            suggestions = []
        
        processor.rebuild()
        processor.sign()
        
        return {
            "status": "success",
            "session_id": session_id,
            "refactor_details": refactor_results,
            "suggestions": suggestions
        }
        
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/api/download/{session_id}")
async def download_apk(session_id: str):
    output_path = f"/app/shared-volume/{session_id}/modified.apk"
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="APK not found")
    return FileResponse(output_path, media_type="application/vnd.android.package-archive", 
                        filename="modified.apk")

@app.delete("/api/cleanup/{session_id}")
async def cleanup_session(session_id: str):
    work_dir = f"/app/shared-volume/{session_id}"
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir)
    return {"status": "cleaned"}
