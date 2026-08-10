from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.jwt_bearer import JWTBearer
from app.routes.face import router as face_router

from app.db import init_db
from app.models.user import User


app = FastAPI()


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

@app.on_event("startup")
def startup():
    print("🚀 Starting Face Authentication API...")

    init_db()

    print("✅ Database initialization completed")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",

        # We will add deployed frontend URL here later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FACE AUTH ROUTES
# ============================================================

app.include_router(face_router)


# ============================================================
# PROTECTED ROUTE
# ============================================================

@app.get(
    "/protected",
    dependencies=[Depends(JWTBearer())]
)
def protected():
    return {
        "message": "You are authorized 🚀"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Face Authentication API is running 🚀"
    }