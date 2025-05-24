from typing import List

from pydantic import BaseModel

class FilmModel(BaseModel):
    name: str
    description: str
    rating: float
    genre: str
    actors: List[str]
    poster: str