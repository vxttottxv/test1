from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import AppException
from app.routers import auth as auth_router
import app.models  # noqa: F401 - 모델 등록

app = FastAPI(
    title="구인구직 API",
    description="구인구직 서비스 백엔드 API",
    version="1.0.0",
)

# ─────────────────────────────────────────────
# CORS 설정 - 프론트엔드 연동
# ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# 전역 예외 핸들러 - 공통 응답 포맷 통일
# ─────────────────────────────────────────────
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.error_message,
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc.errors()),
            },
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 오류가 발생했습니다.",
            },
        },
    )


# ─────────────────────────────────────────────
# 라우터 등록
# ─────────────────────────────────────────────
app.include_router(auth_router.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"success": True, "data": {"status": "ok", "message": "구인구직 API 서버가 실행 중입니다."}}
