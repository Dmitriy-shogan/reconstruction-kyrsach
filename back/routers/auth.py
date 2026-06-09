from fastapi import APIRouter, HTTPException, status
import database
from models import UserCreate, UserLogin, Token
from auth import hash_password, verify_password, create_jwt_token

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE login = %s OR email = %s", (user.login, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    password_hash = hash_password(user.password)
    role = user.role if user.role else 'STUDENT'
    
    cursor.execute(
        "INSERT INTO users (login, password_hash, full_name, email, group_name, role) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
        (user.login, password_hash, user.full_name, user.email, user.group_name, role)
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "User registered successfully", "user_id": user_id}

@router.post("/login")
def login(user: UserLogin):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, password_hash, role FROM users WHERE login = %s", (user.login,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not record or not verify_password(user.password, record[1]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = create_jwt_token(record[0], record[2])
    return Token(access_token=token, token_type="bearer")