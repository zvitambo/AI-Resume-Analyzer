
from dataclasses import dataclass
from typing import List


@dataclass
class Document:
    filename: str
    content: bytes

@dataclass
class ParsedDocument:
    filename: str
    text: str

