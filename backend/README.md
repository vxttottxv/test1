# 구인구직 API (Job Board API)

FastAPI 기반 구인구직 서비스 백엔드입니다.

## 기술 스택

| 구분 | 선택 |
|------|------|
| 프레임워크 | FastAPI |
| ORM | SQLAlchemy 2.0 |
| DB (로컬) | SQLite |
| 인증 | JWT (python-jose) + passlib(bcrypt) |
| 검증 | Pydantic v2 |
| 서버 | Uvicorn |
| 테스트 | pytest + httpx |

## 구현 기능

- [x] 회원가입 (`POST /auth/signup`)
- [x] 로그인 (`POST /auth/login`)
- [x] 토큰 재발급 (`POST /auth/refresh`)
- [x] 로그아웃 (`POST /auth/logout`)
- [ ] 채용공고 목록 조회 (`GET /job-postings`)
- [ ] 채용공고 상세 조회 (`GET /job-postings/{id}`)
- [ ] 지원하기 (`POST /job-postings/{id}/applications`)
- [ ] 내 지원 내역 조회 (`GET /users/me/applications`)

## 로컬 실행 방법

### 1. conda 환경 생성 및 활성화

```bash
conda create -n guinback python=3.11 -y
conda activate guinback
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 파일 생성

```bash
cp .env.example .env
```

> `.env`의 `JWT_SECRET_KEY`를 실제 서비스에서는 반드시 변경하세요.

### 4. DB 테이블 생성

```bash
python -c "
from app.database import Base, engine
import app.models
Base.metadata.create_all(bind=engine)
print('DB 초기화 완료')
"
```

### 5. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. API 문서 확인

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 응답 포맷

모든 API 응답은 공통 포맷을 따릅니다.

### 성공
```json
{
  "success": true,
  "data": { ... }
}
```

### 실패
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "에러 메시지"
  }
}
```

## 주요 에러 코드

| 코드 | 상태 | 설명 |
|------|------|------|
| `EMAIL_ALREADY_EXISTS` | 409 | 중복 이메일 |
| `INVALID_CREDENTIALS` | 401 | 이메일/비밀번호 불일치 |
| `INVALID_TOKEN` | 401 | 유효하지 않은 JWT |
| `FORBIDDEN` | 403 | 권한 없음 |
| `DUPLICATE_APPLICATION` | 409 | 중복 지원 |
| `POSTING_CLOSED` | 400 | 마감된 공고 |

## 테스트 실행

```bash
python -m pytest tests/ -v
```

## 프로젝트 구조

```
guinback/
├── app/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 환경변수 설정
│   ├── database.py          # SQLAlchemy 엔진/세션
│   ├── models/              # DB 모델 (User, Company, JobPosting, Application)
│   ├── schemas/             # Pydantic 요청/응답 DTO
│   ├── routers/             # API 엔드포인트
│   ├── services/            # 비즈니스 로직
│   └── core/                # 보안, 의존성, 예외
├── tests/                   # pytest 테스트
├── .env.example             # 환경변수 템플릿
├── requirements.txt
└── README.md
```
