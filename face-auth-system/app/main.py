from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.auth.jwt_bearer import JWTBearer
from app.routes.face import router as face_router

app = FastAPI()

# Allow React frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Create React App
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include face authentication routes
app.include_router(face_router)

# Protected route
@app.get("/protected", dependencies=[Depends(JWTBearer())])
def protected():
    return {
        "message": "You are authorized 🚀"
    }