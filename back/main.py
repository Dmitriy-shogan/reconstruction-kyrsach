from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from database import init_db
from routers import auth, projects, users, news

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="3D Reconstruction API", lifespan=lifespan)

# Middleware для увеличения размера запроса
@app.middleware("http")
async def increase_body_size(request, call_next):
    request._max_upload_size = 100 * 1024 * 1024  # 100MB
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(users.router)
app.include_router(news.router)

@app.get("/")
def root():
    return {"message": "API is running"}