import asyncio
import logging
from io import BytesIO
from threading import Lock

from faster_whisper import WhisperModel

from app.application.contracts.audio import AudioSample
from app.application.ports.services import Transcriber

from .config import WhisperConfig

logger = logging.getLogger(__name__)


class WhisperTranscriptionAdapter(Transcriber):
    """
    Audio transcription through Faster Whisper
    """

    def __init__(self, config: WhisperConfig) -> None:
        self.config = config
        self.model: WhisperModel | None = None
        self.model_lock = Lock()
        self.transcription_lock = asyncio.Lock()

    def _get_model(self) -> WhisperModel:
        with self.model_lock:
            if self.model is None:
                self.model = WhisperModel(
                    self.config.model,
                    self.config.device,
                )
                logger.info(
                    "Loaded %s Whisper model on %s",
                    self.config.model,
                    self.config.device,
                )
            return self.model

    async def transcribe(self, audio: AudioSample) -> str:
        def run_transcription() -> str:
            segments, _ = self._get_model().transcribe(BytesIO(audio.content))
            return "".join(segment.text for segment in segments)

        async with self.transcription_lock:
            return await asyncio.to_thread(run_transcription)
