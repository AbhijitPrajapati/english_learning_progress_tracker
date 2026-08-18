from dataclasses import dataclass
from typing import ClassVar

from app.application.exceptions import InvalidAudio


@dataclass(frozen=True, slots=True)
class AudioSample:
    MAX_CONTENT_BYTES: ClassVar[int] = 25 * 1024 * 1024

    content: bytes
    filename: str | None
    media_type: str | None

    def __post_init__(self) -> None:
        if not self.content:
            raise InvalidAudio("Audio must not be empty")
        if len(self.content) > self.MAX_CONTENT_BYTES:
            raise InvalidAudio("Audio must be no larger than 25 MiB")
        if self.media_type is None or not self.media_type.startswith("audio/"):
            raise InvalidAudio("An audio content type is required")
        if not self.filename:
            raise InvalidAudio("An audio filename is required")
