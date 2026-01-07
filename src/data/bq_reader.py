from google.cloud import bigquery
import pandas as pd


class BigQueryReader:
    """
    Runs BigQuery jobs in *your* project
    while reading tables from master-ai-cloud
    """

    def __init__(self, job_project: str = "students-group3"):
        self.client = bigquery.Client(project=job_project)

    def fetch_movies(self, limit: int = 100_000) -> pd.DataFrame:
        query = """
        SELECT
            movieId,
            title,
            genres
        FROM `master-ai-cloud.MoviePlatform.movies`
        LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", limit)
            ]
        )
        return self.client.query(query, job_config=job_config).to_dataframe()

    def fetch_ratings(self, limit: int = 500_000) -> pd.DataFrame:
        query = """
        SELECT
            userId,
            movieId,
            rating,
            timestamp
        FROM `master-ai-cloud.MoviePlatform.ratings`
        WHERE rating IS NOT NULL
        LIMIT @limit
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("limit", "INT64", limit)
            ]
        )
        return self.client.query(query, job_config=job_config).to_dataframe()
