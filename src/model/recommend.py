import pandas as pd
import numpy as np
import json

from src.data.gcs_io import GCSReader


class RecommenderService:
    def __init__(self, bucket: str, model_version: str = "v1"):
        self.bucket = bucket
        self.model_version = model_version
        self.reader = GCSReader(bucket)

        self._load_artifacts()

    def _load_artifacts(self):
        print("Loading recommendation artifacts from GCS...")

        self.item_similarity = self.reader.read_parquet(
            f"models/{self.model_version}/item_similarity.parquet"
        )

        self.movie_index = self.reader.read_parquet(
            f"models/{self.model_version}/movie_index.parquet"
        )

        blob = self.reader.bucket.blob("features/popular_movies.json")
        self.popular_movies = json.loads(blob.download_as_text())

        print("Artifacts loaded successfully")

    def recommend(self, user_ratings: dict, top_n: int = 10) -> list:
        """
        user_ratings example:
        { movieId: rating }
        rating in [1..5]
        """

        # -----------------------
        # 1. Cold start
        # -----------------------
        if not user_ratings:
            return self.popular_movies[:top_n]

        # -----------------------
        # 2. Split liked / disliked
        # -----------------------
        liked = {m: r for m, r in user_ratings.items() if r >= 4}
        disliked = {m: r for m, r in user_ratings.items() if r <= 2}

        # If user only rated neutrals (3⭐), fallback to popularity
        if not liked and not disliked:
            return self.popular_movies[:top_n]

        # -----------------------
        # 3. Initialize scores
        # -----------------------
        scores = pd.Series(0.0, index=self.item_similarity.columns)

        # -----------------------
        # 4. Positive signal (liked movies)
        # -----------------------
        for movie_id, rating in liked.items():
            if movie_id in self.item_similarity.index:
                weight = rating / 5.0  # normalize (4⭐≈0.8, 5⭐=1)
                scores += self.item_similarity.loc[movie_id] * weight

        # -----------------------
        # 5. Negative signal (disliked movies)
        # -----------------------
        for movie_id, rating in disliked.items():
            if movie_id in self.item_similarity.index:
                penalty = (3 - rating) / 3.0  # 1⭐=0.66, 2⭐=0.33
                scores -= self.item_similarity.loc[movie_id] * penalty

        # -----------------------
        # 6. Remove already-rated movies
        # -----------------------
        scores = scores.drop(labels=user_ratings.keys(), errors="ignore")

        # -----------------------
        # 7. Rank & select top N
        # -----------------------
        top_items = scores.sort_values(ascending=False).head(top_n)

        if top_items.empty:
            return self.popular_movies[:top_n]

        # -----------------------
        # 8. Map movieId → title
        # -----------------------
        movie_index = self.movie_index.copy()
        movie_index["movieId"] = movie_index["movieId"].astype(int)

        recommendations = movie_index[
            movie_index["movieId"].isin(top_items.index.astype(int))
        ].copy()

        recommendations["score"] = recommendations["movieId"].map(top_items)

        results = [
            {
                "movieId": int(row.movieId),
                "title": row.title,
                "score": float(row.score),
            }
            for row in recommendations.itertuples()
        ]

        return results
