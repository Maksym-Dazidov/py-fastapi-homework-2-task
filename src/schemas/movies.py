import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.database.models import CountryModel, GenreModel, ActorModel, LanguageModel


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str
    status: str
    budget: float
    revenue: float
    country: CountryModel
    genres: list[GenreModel]
    actors: list[ActorModel]
    languages: list[LanguageModel]


class MovieDetail(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieList(BaseModel):
    movies: list[MovieDetail]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str
    status: str
    budget: float
    revenue: float
