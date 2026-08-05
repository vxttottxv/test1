from pydantic import BaseModel, EmailStr, field_validator
from app.models.user import UserType


# ────────────────────────────────────────────
# 회원가입
# ────────────────────────────────────────────
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    user_type: UserType
    name: str | None = None
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("비밀번호는 8자 이상이어야 합니다.")
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    user_type: UserType
    name: str | None = None
    phone: str | None = None

    model_config = {"from_attributes": True}


# ────────────────────────────────────────────
# 로그인
# ────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ────────────────────────────────────────────
# 토큰 재발급
# ────────────────────────────────────────────
class RefreshRequest(BaseModel):
    refresh_token: str
