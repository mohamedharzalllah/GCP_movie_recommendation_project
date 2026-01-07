from pydantic import BaseModel
from typing import Dict, List, Optional


class RateRequest(BaseModel):
    user_id: int
    movie_id: int
    rating: float


class RecommendRequest(BaseModel):
    user_id: int
    top_n: Optional[int] = 10


class Recommendation(BaseModel):
    movieId: int
    title: str
    score: Optional[float] = None
    avg_rating: Optional[float] = None
    rating_count: Optional[int] = None


class RecommendResponse(BaseModel):
    user_id: int
    recommendations: List[Recommendation]
