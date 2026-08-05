"""
tests/test_auth.py
회원가입 / 로그인 / 토큰 재발급 테스트
(DB 설정은 conftest.py에서 처리)
"""
from fastapi.testclient import TestClient


# ─────────────────────────────────────────────────────────────
# 회원가입 테스트
# ─────────────────────────────────────────────────────────────
class TestSignup:
    def test_signup_success_seeker(self, client: TestClient):
        """구직자 회원가입 성공"""
        res = client.post("/auth/signup", json={
            "email": "seeker@test.com",
            "password": "password123",
            "user_type": "SEEKER",
            "name": "홍길동",
            "phone": "010-1234-5678",
        })
        assert res.status_code == 201
        body = res.json()
        assert body["success"] is True
        assert body["data"]["email"] == "seeker@test.com"
        assert body["data"]["user_type"] == "SEEKER"
        assert "password" not in body["data"]      # 비밀번호 미노출 확인

    def test_signup_success_company(self, client: TestClient):
        """기업 회원가입 성공"""
        res = client.post("/auth/signup", json={
            "email": "company@test.com",
            "password": "password123",
            "user_type": "COMPANY",
            "name": "테스트기업",
        })
        assert res.status_code == 201
        body = res.json()
        assert body["success"] is True
        assert body["data"]["user_type"] == "COMPANY"

    def test_signup_duplicate_email(self, client: TestClient):
        """중복 이메일 가입 실패"""
        payload = {
            "email": "dup@test.com",
            "password": "password123",
            "user_type": "SEEKER",
        }
        client.post("/auth/signup", json=payload)
        res = client.post("/auth/signup", json={**payload, "password": "password456"})
        assert res.status_code == 409
        body = res.json()
        assert body["success"] is False
        assert body["error"]["code"] == "EMAIL_ALREADY_EXISTS"

    def test_signup_short_password(self, client: TestClient):
        """비밀번호 8자 미만 → 422 Validation Error"""
        res = client.post("/auth/signup", json={
            "email": "short@test.com",
            "password": "1234567",   # 7자
            "user_type": "SEEKER",
        })
        assert res.status_code == 422

    def test_signup_invalid_email(self, client: TestClient):
        """이메일 형식 오류 → 422"""
        res = client.post("/auth/signup", json={
            "email": "not-an-email",
            "password": "password123",
            "user_type": "SEEKER",
        })
        assert res.status_code == 422


# ─────────────────────────────────────────────────────────────
# 로그인 테스트
# ─────────────────────────────────────────────────────────────
class TestLogin:
    def _create_user(self, client: TestClient, email="user@test.com", password="password123"):
        client.post("/auth/signup", json={
            "email": email,
            "password": password,
            "user_type": "SEEKER",
        })

    def test_login_success(self, client: TestClient):
        """로그인 성공 → access_token, refresh_token 반환"""
        self._create_user(client)
        res = client.post("/auth/login", json={
            "email": "user@test.com",
            "password": "password123",
        })
        assert res.status_code == 200
        body = res.json()
        assert body["success"] is True
        assert "access_token" in body["data"]
        assert "refresh_token" in body["data"]
        assert body["data"]["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient):
        """잘못된 비밀번호 → 401 INVALID_CREDENTIALS"""
        self._create_user(client)
        res = client.post("/auth/login", json={
            "email": "user@test.com",
            "password": "wrongpassword",
        })
        assert res.status_code == 401
        body = res.json()
        assert body["error"]["code"] == "INVALID_CREDENTIALS"

    def test_login_not_found_email(self, client: TestClient):
        """존재하지 않는 이메일 → 401 INVALID_CREDENTIALS"""
        res = client.post("/auth/login", json={
            "email": "notexist@test.com",
            "password": "password123",
        })
        assert res.status_code == 401
        body = res.json()
        assert body["error"]["code"] == "INVALID_CREDENTIALS"


# ─────────────────────────────────────────────────────────────
# 토큰 재발급 테스트
# ─────────────────────────────────────────────────────────────
class TestRefreshToken:
    def _login(self, client: TestClient):
        client.post("/auth/signup", json={
            "email": "refresh@test.com",
            "password": "password123",
            "user_type": "SEEKER",
        })
        res = client.post("/auth/login", json={
            "email": "refresh@test.com",
            "password": "password123",
        })
        return res.json()["data"]

    def test_refresh_success(self, client: TestClient):
        """refresh_token으로 새 access_token 발급"""
        tokens = self._login(client)
        res = client.post("/auth/refresh", json={
            "refresh_token": tokens["refresh_token"]
        })
        assert res.status_code == 200
        body = res.json()
        assert body["success"] is True
        assert "access_token" in body["data"]

    def test_refresh_invalid_token(self, client: TestClient):
        """잘못된 refresh_token → 401"""
        res = client.post("/auth/refresh", json={
            "refresh_token": "invalid.token.here"
        })
        assert res.status_code == 401
        body = res.json()
        assert body["error"]["code"] == "INVALID_TOKEN"
