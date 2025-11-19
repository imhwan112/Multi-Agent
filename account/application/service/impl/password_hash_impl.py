import bcrypt
from account.application.service.password_hash_port import IPasswordHasher

class BcryptHasher(IPasswordHasher):

    def hash(self, password: str) -> str:
        if not password:
            raise ValueError("Password must not be empty.")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
