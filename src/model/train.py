import pandas as pd
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

from src.data.gcs_io import GCSReader, GCSWriter


BUCKET = "students-group3-movie-reco"
MODEL_VERSION = "v1"


def main():
    print("Starting Step 3: Train item-based recommender")

    reader = GCSReader(BUCKET)
    writer = GCSWriter(BUCKET)

    print("Loading curated data...")
    ratings = reader.read_parquet("curated/ratings_clean.parquet")
    movies = reader.read_parquet("curated/movies_clean.parquet")

    print("Building user-item matrix...")
    user_item = ratings.pivot_table(
        index="userId",
        columns="movieId",
        values="rating",
        fill_value=0
    )

    print("Computing item-item cosine similarity...")
    item_similarity = cosine_similarity(user_item.T)

    item_similarity_df = pd.DataFrame(
        item_similarity,
        index=user_item.columns,
        columns=user_item.columns
    )

    print("Saving model artifacts...")
    writer.upload_dataframe_parquet(
        item_similarity_df,
        f"models/{MODEL_VERSION}/item_similarity.parquet"
    )

    writer.upload_dataframe_parquet(
        movies[["movieId", "title"]],
        f"models/{MODEL_VERSION}/movie_index.parquet"
    )

    metadata = {
        "model_type": "item-based-collaborative-filtering",
        "similarity": "cosine",
        "version": MODEL_VERSION,
        "n_users": int(user_item.shape[0]),
        "n_items": int(user_item.shape[1])
    }

    writer.bucket.blob(
        f"models/{MODEL_VERSION}/metadata.json"
    ).upload_from_string(
        json.dumps(metadata, indent=2),
        content_type="application/json"
    )

    print("Step 3 training completed successfully")


if __name__ == "__main__":
    main()
