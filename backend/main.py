from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.jobs import router
from backend.routers import ai
from backend.routers import cv
from backend.routers import auth
from backend.routers import interview
from backend.database.database import init_db

__all__ = ["app"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router, prefix="/jobs")
app.include_router(ai.router)
app.include_router(cv.router)
app.include_router(auth.router)
app.include_router(interview.router)

@app.get("/")
def home():
    return {"message": "Vitej v projektu Kariera+ AI Job Assistant"}