from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, Enum as UserEnum, func
from sqlalchemy.sql import expression
from config.database.session import Base
from account.domain.user_enums import UserRole, ProviderType

# --- [Mixin: 재사용 가능한 컬럼] --- 추후 별도 디렉토리로 분리 필요
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), comment="생성일시")
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now(),comment="수정일시")
    deleted_at = Column(DateTime(timezone=True), nullable=True, comment="삭제 일시")

# 엔티티
class UserOrm(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = {'comment': '회원 테이블'}

    user_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="PK")
    email = Column(String(255), unique=True, nullable=False, index=True, comment="이메일(ID)")
    password = Column(String(255), nullable=True, comment="비밀번호(해시값, 소셜로그인은 NULL)")
    name = Column(String(100), nullable=False, comment="사용자 실명")
    nickname = Column(String(50), nullable=True, unique=True, comment="별명")
    phone_number = Column(String(20), nullable=True, comment="전화번호")
    profile_image_url = Column(String(512), nullable=True, comment="프로필 이미지 URL")
    provider = Column(UserEnum(ProviderType), default=ProviderType.LOCAL, nullable=False, comment="가입 경로")
    social_id = Column(String(255), nullable=True, index=True, comment="소셜 제공자 고유 ID (sub)")
    role = Column(UserEnum(UserRole), default=UserRole.USER, nullable=False, comment="권한")
    last_login_at = Column(DateTime(timezone=True), nullable=True, comment="마지막 로그인 일시")

    # 플래그 성
    active_yn = Column(Boolean, default=True, nullable=False, server_default=expression.true(), comment="계정 활성 여부")
    verified_yn = Column(Boolean, default=False, nullable=False, server_default=expression.false(), comment="이메일 인증 여부")
    agree_yn = Column(Boolean, default=False, nullable=False, server_default=expression.false(),comment="마케팅 수신 동의 여부")
