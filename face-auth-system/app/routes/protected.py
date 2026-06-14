from fastapi import APIRouter, Depends
from app.auth.jwt_bearer import JWTBearer

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/")
def protected_route(token: str = Depends(JWTBearer())):
    return {
        "message": "You are authorized 🚀",
        "token": token
    }