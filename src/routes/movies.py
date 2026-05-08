from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import get_db, MovieModel
from database.models import CountryModel, GenreModel, ActorModel, LanguageModel

from src.schemas.movies import MovieList, MovieCreate, MovieUpdate

router = APIRouter()


@router.get("/movies")
async def get_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20)
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieList(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}")
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    return movie


@router.post("/movies")
async def create_movie(movie_data: MovieCreate, db: AsyncSession = Depends(get_db)):
    movie = MovieModel(
        name=movie_data.name,
        date=movie_data.date,
        score=movie_data.score,
        overview=movie_data.overview,
        status=movie_data.status,
        budget=movie_data.budget,
        revenue=movie_data.revenue,
        country=movie_data.country,
        genres=movie_data.genre,
        actors=movie_data.actor,
        languages=movie_data.language,
    )
    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


@router.patch("/movies/{movie_id}")
async def update_movie(movie_id: int, movie: MovieUpdate, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    movie.name = movie.name
    movie.date = movie.date
    movie.score = movie.score
    movie.overview = movie.overview
    movie.status = movie.status
    movie.budget = movie.budget
    movie.revenue = movie.revenue
    movie.country = movie.country
    movie.genres = movie.genres
    movie.actors = movie.actors
    movie.languages = movie.languages

    db.add(movie)
    await db.commit()
    await db.refresh(movie)
    return movie


@router.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found.")

    movie.delete()
    await db.commit()
    await db.refresh(movie)
    return movie
