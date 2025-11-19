from datetime import datetime
from typing import Optional

from account.infrastructure.orm.user_orm import UserRole, ProviderType

class User:
    def __init__(
            self,
            user_id: Optional[int],
            email: str,
            name: str,
            role: UserRole,
            provider: ProviderType,
            created_at: datetime,
            updated_at: datetime,
            password: Optional[str] = None,
            nickname: Optional[str] = None,
            phone_number: Optional[str] = None,
            profile_image_url: Optional[str] = None,
            social_id: Optional[str] = None,
            active_yn: bool = True,
            verified_yn: bool = False,
            agree_yn: bool = False,
            last_login_at: Optional[datetime] = None,
            deleted_at: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.nickname = nickname
        self.phone_number = phone_number
        self.profile_image_url = profile_image_url
        self.role = role
        self.provider = provider
        self.social_id = social_id
        self.active_yn = active_yn
        self.verified_yn = verified_yn
        self.agree_yn = agree_yn
        self.created_at = created_at
        self.updated_at = updated_at
        self.last_login_at = last_login_at
        self.deleted_at = deleted_at

    @classmethod
    def create(
            cls,
            email: str,
            name: str,
            provider: ProviderType,
            password: Optional[str] = None,
            nickname: Optional[str] = None,
            agree_yn: bool = False,
            social_id: Optional[str] = None,
            profile_image_url: Optional[str] = None
    ) -> "User":

        now = datetime.now()
        return cls(
            user_id=None,
            email=email,
            name=name,
            password=password,
            nickname=nickname,
            role=UserRole.USER,
            provider=provider,
            created_at=now,
            updated_at=now,
            agree_yn=agree_yn,
            social_id=social_id,
            profile_image_url=profile_image_url,
            active_yn=True,
            verified_yn=False
        )
