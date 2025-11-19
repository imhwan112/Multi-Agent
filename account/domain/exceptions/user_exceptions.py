class DomainError(Exception):
    def __init__(self, message: str = "도메인 규칙 위반"):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsError(DomainError):
    def __init__(self, message: str = "사용자가 이미 존재합니다."):
        super().__init__(message)

class UserNotFoundException(DomainError):
    def __init__(self, message: str = "사용자를 찾을 수 없습니다."):
        super().__init__(message)

class InvalidUserDataError(DomainError):
    def __init__(self, message: str = "유효하지 않은 사용자 데이터입니다."):
        super().__init__(message)