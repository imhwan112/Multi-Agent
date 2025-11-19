from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional

from account.domain.user import User
from account.application.port.user_repository_port import UserRepositoryPort
from account.infrastructure.orm.user_orm import UserOrm
from config.database.session import get_db_session
from account.domain.exceptions.user_exceptions import UserNotFoundException

def _to_domain(orm: UserOrm) -> User:
    return User(
        user_id=orm.user_id,
        email=orm.email,
        name=orm.name,
        password=orm.password,
        nickname=orm.nickname,
        phone_number=orm.phone_number,
        profile_image_url=orm.profile_image_url,
        role=orm.role,
        provider=orm.provider,
        social_id=orm.social_id,
        active_yn=orm.active_yn,
        verified_yn=orm.verified_yn,
        agree_yn=orm.agree_yn,
        created_at=orm.created_at,
        updated_at=orm.updated_at,
        last_login_at=orm.last_login_at,
        deleted_at=orm.deleted_at
    )


def _to_orm(user: User, orm_user: Optional[UserOrm] = None) -> UserOrm:
    """User 도메인 객체를 UserOrm 객체로 변환합니다."""
    # 기존 ORM 객체가 있다면 업데이트 모드로 사용
    if orm_user is None:
        orm_user = UserOrm()

    # ID가 None이면 (새로운 유저), ORM 객체에 ID를 설정하지 않음 (DB가 생성)
    if user.user_id is not None:
        orm_user.id = user.user_id

    orm_user.email = user.email
    orm_user.name = user.name
    orm_user.password = user.password
    orm_user.nickname = user.nickname
    orm_user.phone_number = user.phone_number
    orm_user.profile_image_url = user.profile_image_url
    orm_user.role = user.role
    orm_user.provider = user.provider
    orm_user.social_id = user.social_id
    orm_user.active_yn = user.active_yn
    orm_user.verified_yn = user.verified_yn
    orm_user.agree_yn = user.agree_yn
    orm_user.created_at = user.created_at
    orm_user.updated_at = user.updated_at
    orm_user.last_login_at = user.last_login_at
    orm_user.deleted_at = user.deleted_at

    return orm_user

class UserRepositoryImpl(UserRepositoryPort):
    def __init__(self):
        self.db: Session = get_db_session()

    def save(self, user: User) -> User:
        if user.user_id is not None:
            orm_user = self.db.query(UserOrm).get(user.user_id)
            if orm_user is None:
                raise UserNotFoundException(f"User with ID {user.user_id} not found for update.")

            orm_user = _to_orm(user, orm_user)

        else:
            orm_user = _to_orm(user)

        self.db.add(orm_user)
        self.db.commit()
        self.db.refresh(orm_user)

        return _to_domain(orm_user)

    def exists_by_email(self, email: str) -> bool:
        stmt = select(UserOrm).where(
            UserOrm.email == email,
            UserOrm.deleted_at.is_(None)
        )
        return bool(self.db.execute(select(stmt.exists())).scalar_one())

    def find_by_id(self, user_id: int) -> User:
        stmt = select(UserOrm).where(
            UserOrm.user_id == user_id,
            UserOrm.deleted_at.is_(None)
        )
        orm_user = self.db.execute(stmt).scalar_one_or_none()

        if orm_user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found.")

        return _to_domain(orm_user)

    def find_by_email(self, email: str) -> User:
        stmt = select(UserOrm).where(
            UserOrm.email == email,
            UserOrm.deleted_at.is_(None)
        )
        orm_user = self.db.execute(stmt).scalar_one_or_none()

        if orm_user is None:
            raise UserNotFoundException(f"User with email '{email}' not found.")

        return _to_domain(orm_user)

    """
    def list_active_users(self) -> List[User]:
        # 모든 활성 사용자 조회
        stmt = select(UserOrm).where(
            UserOrm.deleted_at.is_(None)
        )
        orm_users = self.db.scalars(stmt).all()

        # 리스트 컴프리헨션을 사용하여 매핑 효율화
        return [_to_domain(orm) for orm in orm_users]
    """