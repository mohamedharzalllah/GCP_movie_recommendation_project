import pandas as pd


def build_popular_movies(
    ratings: pd.DataFrame,
    movies: pd.DataFrame,
    top_n: int = 20,
    min_ratings: int = 50
) -> pd.DataFrame:
    """
    Popularity-based recommender:
    - used for new users (cold start)
    """

    agg = (
        ratings.groupby("movieId")
        .agg(
            avg_rating=("rating", "mean"),
            rating_count=("rating", "count")
        )
        .reset_index()
    )

    agg = agg[agg["rating_count"] >= min_ratings]

    popular = (
        agg.merge(movies, on="movieId", how="inner")
        .sort_values(["avg_rating", "rating_count"], ascending=False)
        .head(top_n)
    )

    return popular[["movieId", "title", "avg_rating", "rating_count"]]
