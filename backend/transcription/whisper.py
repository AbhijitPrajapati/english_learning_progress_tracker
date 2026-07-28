import logging
from typing import BinaryIO

from faster_whisper import WhisperModel

from .config import WhisperConfig

logger = logging.getLogger(__name__)


class WhisperAdapter:
    """
    Audio transcription through Faster Whisper
    """

    def __init__(self, config: WhisperConfig) -> None:
        self.model = WhisperModel(config.model, config.device)
        logger.info("Loaded %s Whisper model on %s", config.model, config.device)

    def transcribe(self, file_stream: BinaryIO) -> str:
        segments, _ = self.model.transcribe(file_stream)
        return "".join([seg.text for seg in segments])
