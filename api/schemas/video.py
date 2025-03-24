from dataclasses import dataclass


@dataclass
class VideoClass:
    name: str
    mime_type: str
    buffer: bytes
