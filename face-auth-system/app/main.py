from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.jwt_bearer import JWTBearer
from app.routes.face import router as face_router

# Database
from app.db import Base, engine

# IMPORTANT:
# Import User so SQLAlchemy knows about the users table
from app.models.user import User


app = FastAPI()


# ==========================================
# CREATE DATABASE TABLES
# ==========================================
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# ==========================================
# CORS
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",

        # Add your deployed frontend URL here later
        # "https://your-frontend.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# FACE AUTH ROUTES
# ==========================================
app.include_router(face_router)


# ==========================================
# PROTECTED ROUTE
# ==========================================
@app.get(
    "/protected",
    dependencies=[Depends(JWTBearer())]
)
def protected():
    return {
        "message": "You are authorized 🚀"
    }


# ==========================================
# HEALTH CHECK
# ==========================================
@app.get("/")
def home():
    return {
        "message": "Face Authentication API is running 🚀"
    }