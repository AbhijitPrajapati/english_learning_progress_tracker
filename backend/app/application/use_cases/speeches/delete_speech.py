from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWork

from .exceptions import SpeechNotFound


class DeleteSpeech:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def execute(self, speech_id: UUID, user_id: UUID) -> None:
        speech = await self.uow.speeches.get(speech_id)
        if speech is None or speech.user_id != user_id:
            raise SpeechNotFound()
        await self.uow.speeches.delete(speech_id)
        await self.uow.commit()
