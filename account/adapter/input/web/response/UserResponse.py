from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# 도메인 모델에 대한 의존성 (웹 어댑터가 도메인 객체를 알 수 있음)
from account.domain.user import User

class UserProfileResponse(BaseModel):
    user_id: int = Field(description="사용자 고유 ID")
    email: str
    name: str
    nickname: Optional[str]
    profile_image_url: Optional[str]
    role: str = Field(description="사용자 권한 (ADMIN, USER)")
    active_yn: bool = Field(description="계정 활성 여부")
    verified_yn: bool = Field(description="이메일 인증 여부")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def from_domain(cls, user: User) -> "UserProfileResponse":
        if user.user_id is None:
            raise ValueError("User ID must not be None for response mapping.")

        return cls(
            user_id=user.user_id,
            email=user.email,
            name=user.name,
            nickname=user.nickname,
            profile_image_url=user.profile_image_url,
            role=user.role.value,
            active_yn=user.active_yn,
            verified_yn=user.verified_yn,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

# 미사용
# class GeneralSuccessResponse(BaseModel):
#     message: str = "요청이 성공적으로 처리되었습니다."
#     success: bool = True