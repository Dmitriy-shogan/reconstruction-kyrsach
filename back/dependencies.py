from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import database
from auth import decode_jwt_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = decode_jwt_token(token)
        user_id = int(payload.get("sub"))
        role = payload.get("role")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, login, role, full_name, email, group_name FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return {
        "id": user[0],
        "login": user[1],
        "role": user[2],
        "full_name": user[3],
        "email": user[4],
        "group_name": user[5]
    }