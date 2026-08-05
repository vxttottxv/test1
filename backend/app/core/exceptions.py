from fastapi import HTTPException, status


class AppException(HTTPException):
    """공통 앱 예외 - 모든 비즈니스 예외는 이것을 상속"""

    def __init__(self, status_code: int, code: str, message: str):
        self.error_code = code
        self.error_message = message
        super().__init__(status_code=status_code, detail={"code": code, "message": message})


class EmailAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="EMAIL_ALREADY_EXISTS",
            message="이미 사용 중인 이메일입니다.",
        )


class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_CREDENTIALS",
            message="이메일 또는 비밀번호가 올바르지 않습니다.",
        )


class InvalidTokenError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="INVALID_TOKEN",
            message="유효하지 않은 토큰입니다.",
        )


class UserNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="USER_NOT_FOUND",
            message="사용자를 찾을 수 없습니다.",
        )


class JobPostingNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="JOB_POSTING_NOT_FOUND",
            message="채용공고를 찾을 수 없습니다.",
        )


class ForbiddenError(AppException):
    def __init__(self, message: str = "권한이 없습니다."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class DuplicateApplicationError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="DUPLICATE_APPLICATION",
            message="이미 지원한 공고입니다.",
        )


class PostingClosedError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="POSTING_CLOSED",
            message="마감된 채용공고입니다.",
        )
