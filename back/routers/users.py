from fastapi import APIRouter, Depends, HTTPException, status
import database
from dependencies import get_current_user
from models import UserResponse, UserUpdate
from auth import hash_password

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    values = []
    
    if user_update.full_name:
        update_fields.append("full_name = %s")
        values.append(user_update.full_name)
    if user_update.email:
        update_fields.append("email = %s")
        values.append(user_update.email)
    if user_update.group_name:
        update_fields.append("group_name = %s")
        values.append(user_update.group_name)
    if user_update.password:
        update_fields.append("password_hash = %s")
        values.append(hash_password(user_update.password))
        
    if not update_fields:
        conn.close()
        return current_user
        
    values.append(current_user['id'])
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING id, login, role, full_name, email, group_name"
    
    cursor.execute(query, tuple(values))
    updated_user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "id": updated_user[0],
        "login": updated_user[1],
        "role": updated_user[2],
        "full_name": updated_user[3],
        "email": updated_user[4],
        "group_name": updated_user[5]
    }