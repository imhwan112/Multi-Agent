import enum

# 유저 타입 / 일반 , 관리자
class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

# 로그인 타입 소셜 로그인인지 / 자체 로그인인지
class ProviderType(str, enum.Enum):
    LOCAL = "local"
    GOOGLE = "google"
    KAKAO = "kakao"
    NAVER = "naver"