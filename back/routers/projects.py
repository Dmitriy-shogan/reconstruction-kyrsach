from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import database
from dependencies import get_current_user
import os
import asyncio

router = APIRouter(prefix="/api/projects", tags=["projects"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    file: UploadFile = File(..., description="ZIP archive with 3D data"),
    current_user: dict = Depends(get_current_user)
):
    # Проверка расширения
    if not file.filename.endswith('.zip'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only ZIP files are allowed"
        )
    
    # Проверка размера (опционально, например 100MB)
    file_size = 0
    content = await file.read()
    file_size = len(content)
    if file_size > 100 * 1024 * 1024:  # 100MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 100MB"
        )
    
    # Сохранение файла
    file_path = os.path.join(UPLOAD_DIR, f"{current_user['id']}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(content)
    
    # Имитация создания проекта
    # (в реальной системе здесь была бы отправка задачи в очередь)
    
    return {
        "project_id": 1,
        "message": "Upload successful, processing started",
        "status": "PROCESSING"
    }