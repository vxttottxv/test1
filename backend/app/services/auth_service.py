from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from jose import JWTError


def signup(db: Session, req: SignupRequest) -> User:
    """
    회원가입 - 이메일 중복 확인 후 bcrypt 해시 저장
    """
    # 이메일 중복 확인
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise EmailAlreadyExistsError()

    user = User(
        email=req.email,
        password_hash=hash_password(req.password),
        user_type=req.user_type,
        name=req.name,
        phone=req.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, req: LoginRequest) -> TokenResponse:
    """
    로그인 - 이메일/비밀번호 검증 후 Access/Refresh Token 반환
    """
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise InvalidCredentialsError()

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def refresh_token(req_refresh_token: str) -> TokenResponse:
    """
    Refresh Token으로 새로운 Access Token 발급
    """
    try:
        payload = decode_token(req_refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidTokenError()
        user_id: str = payload.get("sub")
        if not user_id:
            raise InvalidTokenError()
    except JWTError:
        raise InvalidTokenError()

    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})
    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
