from uuid import UUID

from app.application.ports.services import TokenService

from .models import TokenResponse


class IssueToken:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service = token_service

    async def execute(self, user_id: UUID) -> TokenResponse:
        token = self.token_service.issue(user_id)
        return TokenResponse(access_token=token, user_id=user_id)
