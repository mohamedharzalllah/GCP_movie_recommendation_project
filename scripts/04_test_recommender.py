from src.model.recommend import RecommenderService

BUCKET = "students-group3-movie-reco"

def main():
    recommender = RecommenderService(bucket=BUCKET)

    print("\n--- Cold start recommendations ---")
    cold = recommender.recommend(user_ratings={})
    for r in cold[:5]:
        print(r)

    print("\n--- Warm user recommendations ---")
    user_ratings = {
        1: 5.0,
        50: 4.0,
        100: 3.5
    }

    warm = recommender.recommend(user_ratings=user_ratings)
    for r in warm[:5]:
        print(r)


if __name__ == "__main__":
    main()
