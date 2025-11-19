from abc import ABC, abstractmethod
from typing import Optional

from account.domain.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass

    """
    @abstractmethod
    def list_active_users(self) -> List[User]:
        pass
    """