import streamlit as st
from src.model.recommend import RecommenderService
import streamlit as st

# ---------------------------
# Session state initialization
# ---------------------------
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "recommendations" not in st.session_state:
    st.session_state["recommendations"] = []


BUCKET = "students-group3-movie-reco"
TOP_N = 20

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

# -------------------------------------------------
# Initialize global users table
# -------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {}  # { user_id: { "ratings": {} } }

# -------------------------------------------------
# Helper functions
# -------------------------------------------------
from src.data.ratings_repository import RatingsRepository

ratings_repo = RatingsRepository()

def get_or_create_user(user_id: int):
    if user_id not in st.session_state.users:
        db_ratings = ratings_repo.get_user_ratings(user_id)

        st.session_state.users[user_id] = {
            "db_ratings": db_ratings,
            "session_ratings": {}
        }

    return st.session_state.users[user_id]

def add_rating(user_id: int, movie_id: int, rating: int):
    st.session_state.users[user_id]["session_ratings"][movie_id] = rating

def get_effective_ratings(user):
    # session ratings override DB ratings
    return {**user["db_ratings"], **user["session_ratings"]}


# -------------------------------------------------
# Load recommender once
# -------------------------------------------------
@st.cache_resource
def load_recommender():
    return RecommenderService(bucket=BUCKET)

recommender = load_recommender()

# -------------------------------------------------
# User selection UI
# -------------------------------------------------
st.sidebar.header("👤 User Selection")

user_id = st.sidebar.number_input(
    "Enter User ID",
    min_value=1,
    step=1
)

user = get_or_create_user(user_id)

st.sidebar.success(f"Active user: {user_id}")

# -------------------------------------------------
# Recommendations
# -------------------------------------------------
st.subheader("🎯 Recommended Movies")

effective_ratings = get_effective_ratings(user)

recommendations = recommender.recommend(
    user_ratings=effective_ratings,
    top_n=TOP_N
)
rated_movie_ids = set(get_effective_ratings(user).keys())

recommendations = [
    movie for movie in recommendations
    if "movieId" in movie and movie["movieId"] not in rated_movie_ids
]


for movie in recommendations:
    movie_id = int(movie["movieId"])
    title = movie["title"]

    col1, col2 = st.columns([4, 2])

    with col1:
        st.markdown(f"**🎥 {title}**")

    with col2:
        rating_key = f"rating_{user_id}_{movie_id}"

        st.radio(
            label=f"Rate {title}",
            options=[0, 1, 2, 3, 4, 5],
            index=st.session_state["ratings"].get(movie_id, 0),
            format_func=lambda x: "⭐" * x if x > 0 else "Not rated",
            key=rating_key,
            horizontal=True,
            label_visibility="collapsed",
            on_change=lambda mid=movie_id, key=rating_key: add_rating(
                user_id, mid, st.session_state[key]
            ),
        )


# -------------------------------------------------
# Rated movies section
# -------------------------------------------------
st.subheader("✅ Movies Rated by User")

effective_ratings = get_effective_ratings(user)

if effective_ratings:
    for movie_id, rating in effective_ratings.items():
        title = recommender.movie_index.loc[
            recommender.movie_index["movieId"] == movie_id,
            "title"
        ].values[0]

        source = (
            "🗄️ DB" if movie_id in user["db_ratings"]
            else "🆕 Session"
        )

        st.markdown(f"🎬 **{title}** — ⭐ {rating} ({source})")
else:
    st.info("This user has not rated any movies yet.")
