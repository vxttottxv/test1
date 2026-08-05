from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import SignupRequest, LoginRequest, RefreshRequest, UserResponse, TokenResponse
from app.services import auth_service
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    user = auth_service.signup(db, req)
    return {"success": True, "data": UserResponse.model_validate(user)}


@router.post(
    "/login",
    summary="로그인",
)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    tokens = auth_service.login(db, req)
    return {"success": True, "data": tokens}


@router.post(
    "/refresh",
    summary="Access Token 재발급",
)
def refresh(req: RefreshRequest):
    tokens = auth_service.refresh_token(req.refresh_token)
    return {"success": True, "data": tokens}


@router.post(
    "/logout",
    summary="로그아웃 (클라이언트 토큰 삭제 안내)",
)
def logout(_current_user: User = Depends(get_current_user)):
    # 서버 사이드 상태 없음 (JWT 무상태). 클라이언트에서 토큰 삭제 필요.
    return {"success": True, "data": {"message": "로그아웃 되었습니다. 클라이언트에서 토큰을 삭제하세요."}}
