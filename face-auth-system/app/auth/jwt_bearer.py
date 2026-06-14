from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.jwt_handler import decode_token


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            try:
                # Verify token
                decode_token(credentials.credentials)
                return credentials.credentials
            except Exception:
                raise HTTPException(status_code=403, detail="Invalid token")

        raise HTTPException(status_code=403, detail="Invalid authorization")