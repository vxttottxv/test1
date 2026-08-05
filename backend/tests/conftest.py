"""
tests/conftest.py
인메모리 SQLite는 커넥션이 닫히면 데이터가 사라짐.
StaticPool로 항상 같은 커넥션을 재사용하도록 설정.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

# StaticPool: 모든 세션이 같은 인메모리 커넥션을 공유
engine_test = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

# 모델 메타데이터 등록 (Base에 테이블 정의 로드)
import app.models  # noqa: F401, E402
from app.database import Base, get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


fastapi_app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def setup_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def client(setup_db):
    """setup_db에 의존 → 테이블 보장 후 클라이언트 반환"""
    with TestClient(fastapi_app) as c:
        yield c
