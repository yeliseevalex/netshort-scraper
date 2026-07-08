from dataclasses import dataclass
from typing import Optional


@dataclass
class Series:
    title: str
    url: str
    cover_image: Optional[str]
    description: Optional[str]
    genre: Optional[str]
    episodes: Optional[int]
    status: Optional[str]
    tags: Optional[str]