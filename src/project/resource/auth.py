from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from project.resource.jwt_token import decode_access_token, TokenData
from project.core.config import settings

security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = decode_access_token(
            token=token.credentials,
            secret=settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.HASH_ALGORITHM
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


async def allow_only_admin(current_user: TokenData = Depends(get_current_user)):
    if current_user.is_admin == False:
        raise HTTPException(status_code=403, detail="Access forbidden: Admins only")
    return current_user