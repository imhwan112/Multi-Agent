from pydantic import BaseModel, Field
from typing import Optional

# ----------------------------------------------------
# 1. 회원가입 요청 (POST /users/register)
# ----------------------------------------------------
class UserRegisterRequest(BaseModel):
    email: str = Field(..., max_length=255, description="사용자 이메일 (유니크)")
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자 이상)")
    name: str = Field(..., max_length=100, description="사용자 실명")

    nickname: Optional[str] = Field(None, max_length=50, description="별명")
    agree_marketing: bool = Field(False, description="마케팅 수신 동의 여부")

    class Config:
        extra = 'forbid'


# ----------------------------------------------------
# 2. 프로필 수정 요청 (PUT /users/me) (미구현)
# ----------------------------------------------------
# class UserUpdateRequest(BaseModel):
#     name: Optional[str] = Field(None, max_length=100)
#     nickname: Optional[str] = Field(None, max_length=50)
#     phone_number: Optional[str] = Field(None, max_length=20)
#     profile_image_url: Optional[str] = Field(None, max_length=512)
#
#     class Config:
#         extra = 'forbid'


# ----------------------------------------------------
# 3. 비밀번호 변경 요청 (POST /users/me/password) (미구현)
# ----------------------------------------------------
# class UserPasswordChangeRequest(BaseModel):
#     current_password: str = Field(..., description="현재 비밀번호")
#     new_password: str = Field(..., min_length=8, description="새 비밀번호 (최소 8자 이상)")
#
#     class Config:
#         extra = 'forbid'