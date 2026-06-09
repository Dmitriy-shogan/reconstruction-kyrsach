from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    login: str
    password: str
    full_name: str
    email: EmailStr
    group_name: str
    role: Optional[str] = 'STUDENT'

class UserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    login: str
    full_name: str
    email: str
    group_name: str
    role: str

class ProjectResponse(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

class ProjectDetailResponse(ProjectResponse):
    progress_percent: int
    result_path: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    group_name: Optional[str] = None
    password: Optional[str] = None

class NewsCreate(BaseModel):
    title: str
    content: str