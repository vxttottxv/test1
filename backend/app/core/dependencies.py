from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.core.exceptions import InvalidTokenError, UserNotFoundError
from app.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """JWT 토큰에서 현재 유저를 추출하는 FastAPI Depends"""
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise InvalidTokenError()
        user_id: int = payload.get("sub")
        if user_id is None:
            raise InvalidTokenError()
    except JWTError:
        raise InvalidTokenError()

    user = db.get(User, int(user_id))
    if user is None:
        raise UserNotFoundError()

    return user
