from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork
from app.domain.speech import SpeechId

from .exceptions import SpeechNotFound


class DeleteSpeech:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, speech_id: UUID, user_id: UUID) -> None:
        domain_speech_id = SpeechId(value=speech_id)
        speech = await self.uow.speeches.get(domain_speech_id)
        if speech is None or speech.user_id.value != user_id:
            raise SpeechNotFound()
        await self.uow.speeches.delete(domain_speech_id)
        await self.uow.commit()
