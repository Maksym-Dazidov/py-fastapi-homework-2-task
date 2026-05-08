import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.database.models import CountryModel, MovieStatusEnum


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float
    revenue: float
    country: CountryModel
    genres: list[str]
    actors: list[str]
    languages: list[str]


class MovieDetail(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieListItem(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    overview: str


class MovieList(BaseModel):
    movies: list[MovieListItem]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    name: Optional[str]
    date: Optional[datetime.date]
    score: Optional[float]
    overview: Optional[str]
    status: Optional[str]
    budget: Optional[float]
    revenue: Optional[float]
