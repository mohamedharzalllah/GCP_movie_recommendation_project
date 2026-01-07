import pandas as pd


def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["movieId", "title"])
    df["movieId"] = df["movieId"].astype(int)
    return df


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["userId", "movieId", "rating"])
    df = df[df["rating"].between(0.5, 5.0)]
    df["userId"] = df["userId"].astype(int)
    df["movieId"] = df["movieId"].astype(int)
    return df
