from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.auth.jwt_handler import create_access_token

import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO

router = APIRouter(
    prefix="/face",
    tags=["Face Authentication"]
)


# ==========================
# GET FACE ENCODING
# ==========================
def get_face_encoding(image):
    """
    Returns the face encoding of the first detected face.
    """

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        return None

    return encodings[0]


# ==========================
# COMPARE TWO FACES
# ==========================
def compare_faces(known_encoding, unknown_encoding):
    """
    Returns True if both faces match.
    """

    return face_recognition.compare_faces(
        [known_encoding],
        unknown_encoding,
        tolerance=0.5
    )[0]


# ==========================
# REGISTER
# ==========================
@router.post("/register")
async def register(
    name: str,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    # Validate name
    if not name or not name.strip():
        raise HTTPException(
            status_code=400,
            detail="Name cannot be empty."
        )

    name = name.strip()

    # Check existing user
    existing = db.query(User).filter(User.name == name).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists."
        )

    try:
        contents = await file.read()

        image = Image.open(BytesIO(contents)).convert("RGB")
        image = np.array(image)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image uploaded."
        )

    encoding = get_face_encoding(image)

    if encoding is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected."
        )

    new_user = User(
        name=name,
        face_encoding=encoding.tobytes()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully.",
        "username": new_user.name
    }


# ==========================
# LOGIN
# ==========================
@router.post("/login")
async def login(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()

        image = Image.open(BytesIO(contents)).convert("RGB")
        image = np.array(image)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image uploaded."
        )

    unknown_encoding = get_face_encoding(image)

    if unknown_encoding is None:
        raise HTTPException(
            status_code=400,
            detail="No face detected."
        )

    users = db.query(User).all()

    if len(users) == 0:
        raise HTTPException(
            status_code=404,
            detail="No registered users found."
        )

    for user in users:

        known_encoding = np.frombuffer(
            user.face_encoding,
            dtype=np.float64
        )

        matched = compare_faces(
            known_encoding,
            unknown_encoding
        )

        if matched:

            token = create_access_token(
                {
                    "sub": user.name
                }
            )

            return {
                "success": True,
                "message": "Login successful.",
                "username": user.name,
                "access_token": token,
                "token_type": "bearer"
            }

    raise HTTPException(
        status_code=401,
        detail="Face not recognized."
    )