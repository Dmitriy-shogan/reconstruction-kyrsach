import os
import asyncio
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
import database
from dependencies import get_current_user
from models import ProjectResponse, ProjectDetailResponse

router = APIRouter(prefix="/api/projects", tags=["projects"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def mock_reconstruction(project_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    for progress in range(0, 101, 20):
        await asyncio.sleep(2)
        status_val = "PROCESSING" if progress < 100 else "DONE"
        result = "/models/cube.obj" if progress == 100 else None
        
        cursor.execute(
            "UPDATE reconstruction_jobs SET progress_percent = %s, status = %s, result_path = %s, updated_at = CURRENT_TIMESTAMP WHERE project_id = %s",
            (progress, status_val, result, project_id)
        )
        conn.commit()
        
    cursor.execute(
        "UPDATE projects SET status = 'DONE' WHERE id = %s",
        (project_id,)
    )
    
    cursor.execute(
        "INSERT INTO email_logs (user_id, subject, status) SELECT user_id, 'Reconstruction Complete', 'SENT' FROM projects WHERE id = %s",
        (project_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only ZIP files are allowed")
    
    file_path = os.path.join(UPLOAD_DIR, f"{current_user['id']}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO projects (user_id, title, archive_path, status) VALUES (%s, %s, %s, 'PENDING') RETURNING id",
        (current_user['id'], file.filename, file_path)
    )
    project_id = cursor.fetchone()[0]
    
    cursor.execute(
        "INSERT INTO reconstruction_jobs (project_id, status, progress_percent) VALUES (%s, 'QUEUED', 0)",
        (project_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    asyncio.create_task(mock_reconstruction(project_id))
    
    return {"project_id": project_id, "message": "Upload successful, processing started"}

@router.get("/", response_model=list[ProjectResponse])
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

@router.get("/{project_id}", response_model=ProjectDetailResponse)
def get_project_detail(project_id: int, current_user: dict = Depends(get_current_user)):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.id, p.title, p.status, p.created_at, r.progress_percent, r.result_path 
        FROM projects p
        JOIN reconstruction_jobs r ON p.id = r.project_id
        WHERE p.id = %s AND (p.user_id = %s OR %s IN ('STAROSTA', 'ADMIN'))
    """, (project_id, current_user['id'], current_user['role']))
    
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    return {
        "id": record[0],
        "title": record[1],
        "status": record[2],
        "created_at": record[3],
        "progress_percent": record[4],
        "result_path": record[5]
    }