# 구인구직 플랫폼

## 프로젝트 구조

```
test1/
├── backend/    # FastAPI (Python)
└── frontend/   # React + Vite + TypeScript
```

## 백엔드 실행

```bash
cd backend

# 가상환경 생성 & 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행 (http://localhost:8000)
uvicorn app.main:app --reload
```

## 프론트엔드 실행

```bash
cd frontend

# 패키지 설치 (처음 한 번만)
npm install

# 개발 서버 실행 (http://localhost:5173)
npm run dev
```

## API 문서

백엔드 실행 후 → http://localhost:8000/docs
