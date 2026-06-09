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
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        # Проверка расширения
        if not file.filename or not file.filename.endswith('.zip'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only ZIP files are allowed"
            )
        
        # Чтение файла
        content = await file.read()
        
        # Проверка размера (максимум 50MB)
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size must be less than 50MB"
            )
        
        # Сохранение файла
        file_path = os.path.join(UPLOAD_DIR, f"{current_user['id']}_{file.filename}")
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        # Создание записи в БД
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO projects (user_id, title, archive_path, status) 
               VALUES (%s, %s, %s, 'PENDING') RETURNING id""",
            (current_user['id'], file.filename, file_path)
        )
        project_id = cursor.fetchone()[0]
        
        cursor.execute(
            """INSERT INTO reconstruction_jobs (project_id, status, progress_percent) 
               VALUES (%s, 'QUEUED', 0)""",
            (project_id,)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Запуск фоновой обработки
        asyncio.create_task(mock_reconstruction(project_id))
        
        return JSONResponse(
            status_code=201,
            content={
                "project_id": project_id,
                "message": "Upload successful",
                "status": "PENDING"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

async def mock_reconstruction(project_id: int):
    """Имитация процесса реконструкции"""
    try:
        conn = database.get_db_connection()
        cursor = conn.cursor()
        
        for progress in [20, 40, 60, 80, 100]:
            await asyncio.sleep(2)
            status_val = "PROCESSING" if progress < 100 else "DONE"
            result = "/models/cube.obj" if progress == 100 else None
            
            cursor.execute(
                """UPDATE reconstruction_jobs 
                   SET progress_percent = %s, status = %s, result_path = %s, updated_at = CURRENT_TIMESTAMP 
                   WHERE project_id = %s""",
                (progress, status_val, result, project_id)
            )
            conn.commit()
        
        cursor.execute("UPDATE projects SET status = 'DONE' WHERE id = %s", (project_id,))
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Reconstruction error: {str(e)}")

@router.get("/")
def get_projects(current_user: dict = Depends(get_current_user)):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    if current_user['role'] in ['STAROSTA', 'ADMIN']:
        cursor.execute("SELECT id, title, status, created_at FROM projects ORDER BY created_at DESC")
    else:
        cursor.execute(
            "SELECT id, title, status, created_at FROM projects WHERE user_id = %s ORDER BY created_at DESC",
            (current_user['id'],)
        )
    
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [{"id": p[0], "title": p[1], "status": p[2], "created_at": p[3]} for p in projects]