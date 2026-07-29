import logging
from typing import BinaryIO

from faster_whisper import WhisperModel

from application.samples.transcription import TranscriptionAdapter
from infrastructure.config.whisper import WhisperConfig

logger = logging.getLogger(__name__)


class TranscriptionError(Exception):
    pass


class WhisperTranscriptionAdapter(TranscriptionAdapter):
    """
    Audio transcription through Faster Whisper
    """

    def __init__(self, config: WhisperConfig) -> None:
        try:
            self.model = WhisperModel(config.model, config.device)
        except Exception as e:
            raise TranscriptionError("Failed to load transcription model") from e
        logger.info("Loaded %s Whisper model on %s", config.model, config.device)

    def transcribe(self, file_stream: BinaryIO) -> str:
        try:
            segments, _ = self.model.transcribe(file_stream)
            return "".join([seg.text for seg in segments])
        except Exception as e:
            logger.exception("Transcription failed")
            raise TranscriptionError() from e
