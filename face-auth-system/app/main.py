from fastapi import FastAPI, Depends
from app.auth.jwt_bearer import JWTBearer

# ✅ IMPORT YOUR ROUTER
from app.routes.face import router as face_router

app = FastAPI()

# ✅ INCLUDE ROUTER
app.include_router(face_router)

@app.get("/protected", dependencies=[Depends(JWTBearer())])
def protected():
    return {"message": "You are authorized 🚀"}