import pandas as pd
from google.cloud import bigquery

class RatingsRepository:
    def __init__(self):
        self.client = bigquery.Client()

    def get_user_ratings(self, user_id: int) -> dict:
        query = """
            SELECT movieId, rating
            FROM `master-ai-cloud.MoviePlatform.ratings`
            WHERE userId = @user_id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "INT64", user_id)
            ]
        )

        df = self.client.query(query, job_config=job_config).to_dataframe()

        return dict(zip(df["movieId"], df["rating"]))
