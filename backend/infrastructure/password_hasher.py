from pwdlib import PasswordHash

from application.users.password_hasher import PasswordHasher


class PwdLibPasswordHasher(PasswordHasher):
    def __init__(self) -> None:
        self.password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify(self, password: str, password_hash: str) -> bool:
        return self.hash(password) == password_hash
