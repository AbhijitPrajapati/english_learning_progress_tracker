from app.application.ports.services import TokenService
from app.domain.user import UserId


class IssueToken:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service = token_service

    async def execute(self, user_id: UserId) -> str:
        return self.token_service.issue(user_id)
