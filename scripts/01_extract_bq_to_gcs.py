from src.data.bq_reader import BigQueryReader
from src.data.gcs_io import GCSWriter


BUCKET_NAME = "students-group3-movie-reco"

def main():
    print("Starting BigQuery → GCS ingestion")

    bq = BigQueryReader()
    gcs = GCSWriter(bucket_name=BUCKET_NAME)

    print("Fetching movies...")
    movies_df = bq.fetch_movies()
    print(f"Movies fetched: {movies_df.shape}")

    print("Fetching ratings...")
    ratings_df = bq.fetch_ratings()
    print(f"Ratings fetched: {ratings_df.shape}")

    print("Uploading movies to GCS...")
    gcs.upload_dataframe_parquet(
        movies_df,
        "raw/movies.parquet"
    )

    print("Uploading ratings to GCS...")
    gcs.upload_dataframe_parquet(
        ratings_df,
        "raw/ratings.parquet"
    )

    print("Step 1 completed successfully")


if __name__ == "__main__":
    main()
