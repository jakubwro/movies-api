from dataclasses import dataclass
from typing import List

@dataclass
class Movie:
    id: str
    title: str
    average_rating: float
    length_in_minutes: float
    directors: List[str]
    writers: List[str]
    actors: List[str]
