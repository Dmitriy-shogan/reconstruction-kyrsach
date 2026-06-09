from fastapi import APIRouter, Depends, HTTPException, status
import database
from dependencies import get_current_user
from models import NewsCreate

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/")
def get_news(current_user: dict = Depends(get_current_user)):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, created_at FROM news ORDER BY created_at DESC LIMIT 10")
    news_items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [{"id": n[0], "title": n[1], "content": n[2], "created_at": n[3]} for n in news_items]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_news(news: NewsCreate, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут создавать новости")
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO news (title, content, author_id) VALUES (%s, %s, %s) RETURNING id",
        (news.title, news.content, current_user['id'])
    )
    news_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"id": news_id, "message": "Новость создана"}

@router.delete("/{news_id}")
def delete_news(news_id: int, current_user: dict = Depends(get_current_user)):
    if current_user['role'] != 'ADMIN':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только администраторы могут удалять новости")
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id = %s AND author_id = %s", (news_id, current_user['id']))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Новость удалена"}