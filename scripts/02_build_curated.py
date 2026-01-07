import json

from src.data.gcs_io import GCSReader, GCSWriter
from src.data.validate import clean_movies, clean_ratings
from src.features.cold_start import build_popular_movies


BUCKET = "students-group3-movie-reco"


def main():
    print("Starting Step 2: Curated layer & cold-start")

    reader = GCSReader(BUCKET)
    writer = GCSWriter(BUCKET)

    print("Loading RAW data from GCS...")
    movies = reader.read_parquet("raw/movies.parquet")
    ratings = reader.read_parquet("raw/ratings.parquet")

    print("Cleaning data...")
    movies_clean = clean_movies(movies)
    ratings_clean = clean_ratings(ratings)

    print("Saving curated datasets...")
    writer.upload_dataframe_parquet(
        movies_clean,
        "curated/movies_clean.parquet"
    )
    writer.upload_dataframe_parquet(
        ratings_clean,
        "curated/ratings_clean.parquet"
    )

    print("Building cold-start popular movies...")
    popular = build_popular_movies(ratings_clean, movies_clean)

    popular_json = popular.to_dict(orient="records")

    writer.bucket.blob("features/popular_movies.json").upload_from_string(
        json.dumps(popular_json, indent=2),
        content_type="application/json"
    )

    print("Step 2 completed successfully")


if __name__ == "__main__":
    main()
