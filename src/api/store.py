from collections import defaultdict


class RatingStore:
    """
    Simple in-memory store:
    user_id -> { movie_id: rating }
    """

    def __init__(self):
        self._ratings = defaultdict(dict)

    def add_rating(self, user_id: int, movie_id: int, rating: float):
        self._ratings[user_id][movie_id] = rating

    def get_user_ratings(self, user_id: int) -> dict:
        return self._ratings.get(user_id, {})
