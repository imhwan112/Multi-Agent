from typing import Optional, List
from account.application.port.user_repository_port import UserRepositoryPort
from account.domain.user import User
from account.domain.user_enums import ProviderType
from account.domain.exceptions.user_exceptions import UserAlreadyExistsError, UserNotFoundException


class UserUseCase:
    def __init__(self, user_repo: UserRepositoryPort):
        self.user_repo = user_repo

    def register_user(
            self,
            email: str,
            hashed_password: str,
            name: str,
            provider: ProviderType = ProviderType.LOCAL,
            nickname: Optional[str] = None,
            agree_yn: bool = False
    ) -> User:

        if self.user_repo.exists_by_email(email):
            raise UserAlreadyExistsError(f"Email {email} is already taken.")

        new_user = User.create(
            email=email,
            password=hashed_password,
            name=name,
            provider=provider,
            nickname=nickname,
            agree_yn=agree_yn
        )

        return self.user_repo.save(new_user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.find_by_email(email)
        if user is None:
            raise UserNotFoundException(f"User with email {email} not found.")
        return user

    """
    ## --- 프로필 수정 로직 --- 미구현
    def update_user_profile(
            self,
            user_id: int,
            name: Optional[str] = None,
            nickname: Optional[str] = None,
            phone_number: Optional[str] = None,
            profile_image_url: Optional[str] = None
    ) -> User:

        user = self.get_user_profile(user_id)

        user.update_profile(
            name=name if name is not None else user.name,
            nickname=nickname if nickname is not None else user.nickname,
            phone_number=phone_number,
            profile_image_url=profile_image_url,
        )

        return self.user_repo.save(user)

    ## 미구현
    def list_all_active_users(self) -> List[User]:
        return self.user_repo.list_active_users()

    ## 미구현
    def change_password(
            self,
            user: User,
            current_password: str,
            new_password: str,
            hasher: IPasswordHasher  # 라우터에서 DI 받은 Hasher를 인자로 받음
    ) -> None:

        if not user.check_password(current_password, hasher):
            raise ValueError("현재 비밀번호가 일치하지 않습니다.")

        new_hashed_password = hasher.hash(new_password)

        user.change_password(new_hashed_password)

        # 4. 영속성 처리
        self.user_repo.save(user)
    """
