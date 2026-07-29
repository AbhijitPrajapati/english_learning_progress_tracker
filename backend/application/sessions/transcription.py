from typing import BinaryIO, Protocol


class TranscriptionAdapter(Protocol):
    def transcribe(self, file_stream: BinaryIO) -> str: ...
