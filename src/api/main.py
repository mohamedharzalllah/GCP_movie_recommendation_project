from fastapi import FastAPI, HTTPException

from src.model.recommend import RecommenderService
from src.api.schemas import (
    RateRequest,
    RecommendRequest,
    RecommendResponse,
)
from src.api.store import RatingStore


BUCKET = "students-group3-movie-reco"

app = FastAPI(
    title="Movie Recommendation API",
    version="1.0.0",
    root_path="/proxy/8000"
)

# Initialize services once at startup
recommender = RecommenderService(bucket=BUCKET)
rating_store = RatingStore()


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/rate")
def rate_movie(request: RateRequest):
    if not (0.5 <= request.rating <= 5.0):
        raise HTTPException(status_code=400, detail="Rating must be between 0.5 and 5")

    rating_store.add_rating(
        user_id=request.user_id,
        movie_id=request.movie_id,
        rating=request.rating
    )

    return {
        "message": "Rating stored",
        "user_id": request.user_id,
        "movie_id": request.movie_id,
        "rating": request.rating
    }


@app.post("/recommend", response_model=RecommendResponse)
def recommend_movies(request: RecommendRequest):
    user_ratings = rating_store.get_user_ratings(request.user_id)

    recommendations = recommender.recommend(
        user_ratings=user_ratings,
        top_n=request.top_n
    )

    return {
        "user_id": request.user_id,
        "recommendations": recommendations
    }
