import logging
from io import BytesIO

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
        self.model = WhisperModel(config.model, config.device)
        logger.info("Loaded %s Whisper model on %s", config.model, config.device)

    async def transcribe(self, audio: AudioSample) -> str:
        segments, _ = self.model.transcribe(BytesIO(audio.content))
        return "".join(segment.text for segment in segments)
