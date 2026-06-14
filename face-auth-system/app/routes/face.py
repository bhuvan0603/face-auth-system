from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User

import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO

# ✅ JWT
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/face", tags=["Face Auth"])


# =========================
# FACE ENCODING FUNCTION
# =========================
def get_face_encoding(image):
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0]


# =========================
# FACE COMPARISON FUNCTION
# =========================
def compare_faces(known, unknown):
    return face_recognition.compare_faces([known], unknown)[0]


# =========================
# REGISTER
# =========================
@router.post("/register")
async def register(name: str, file: UploadFile, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    contents = await file.read()
    image = Image.open(BytesIO(contents))
    image = np.array(image)

    encoding = get_face_encoding(image)
    if encoding is None:
        raise HTTPException(status_code=400, detail="No face detected")

    user = User(
        name=name,
        face_encoding=encoding.tobytes()
    )

    db.add(user)
    db.commit()

    return {"message": "User registered"}


# =========================
# LOGIN
# =========================
@router.post("/login")
async def login(file: UploadFile, db: Session = Depends(get_db)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))
    image = np.array(image)

    unknown_encoding = get_face_encoding(image)
    if unknown_encoding is None:
        raise HTTPException(status_code=400, detail="No face detected")

    users = db.query(User).all()

    for user in users:
        known_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)

        if compare_faces(known_encoding, unknown_encoding):
            token = create_access_token({"sub": user.name})
            return {
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(status_code=401, detail="Face not recognized")