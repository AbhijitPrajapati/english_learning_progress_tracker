from uuid import UUID

from app.application.ports.unit_of_work import UnitOfWorkFactory

from .exceptions import SpeechNotFound


class DeleteSpeech:
    def __init__(self, uow_factory: UnitOfWorkFactory) -> None:
        self.uow_factory = uow_factory

    async def execute(self, speech_id: UUID, user_id: UUID) -> None:
        async with self.uow_factory() as uow:
            speech = await uow.speeches.get(speech_id)
            if speech is None or speech.user_id != user_id:
                raise SpeechNotFound()
            await uow.speeches.delete(speech_id)
            await uow.commit()
