```text
GCP_movie_recommendation_project/
│
├── scripts/                         # Pipeline execution scripts
│   ├── 00_sanity_check.py           # GCP connectivity check
│   ├── 01_extract_bq_to_gcs.py      # BigQuery → GCS ingestion
│   ├── 02_build_curated.py          # Data cleaning & cold start
│   └── 04_test_recommender.py       # Local recommender testing
│
├── src/
│   ├── api/                         # API layer (FastAPI)
│   │   ├── main.py                  # API endpoints
│   │   ├── schemas.py               # Request / response schemas
│   │   └── store.py                 # In-memory rating store
│   │
│   ├── data/                        # Data access & validation
│   │   ├── bq_reader.py             # BigQuery access
│   │   ├── gcs_io.py                # GCS read/write utilities
│   │   ├── ratings_repository.py    # User ratings from BigQuery
│   │   └── validate.py              # Data cleaning & validation
│   │
│   ├── features/                    # Feature engineering
│   │   └── cold_start.py            # Popularity-based recommender
│   │
│   ├── model/                       # Training & inference
│   │   ├── train.py                 # Model training
│   │   └── recommend.py             # Recommendation logic
│   │
│   └── __init__.py
│
├── streamlit_app.py                 # Interactive UI
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
└── .gitignore



🔄 End-to-End Workflow

Step 0 – Environment Sanity Check**
**Script:** `scripts/00_sanity_check.py`

- Verifies access to:
  - BigQuery
  - Cloud Storage
- Ensures credentials and permissions are correctly configured

✅ Prevents silent failures later in the pipeline.

---

Step 1 – Data Ingestion (BigQuery → GCS)**
**Script:** `scripts/01_extract_bq_to_gcs.py`

- Reads:
  - `movies` table
  - `ratings` table
- Source dataset: `master-ai-cloud.MoviePlatform`
- Stores raw datasets as **Parquet files** in GCS:

✅ Parquet is used for performance and ML-readiness.

---

Step 2 – Data Cleaning & Cold-Start Features**
**Script:** `scripts/02_build_curated.py`

#### Data Cleaning
- Removes null values
- Enforces correct data types
- Filters invalid ratings

**Outputs:**
curated/movies_clean.parquet
curated/ratings_clean.parquet

#### Cold-Start Strategy
- Computes most popular movies
- Based on:
  - Average rating
  - Number of ratings
- Stored as:

✅ Guarantees recommendations for new users with no history.

---

Step 3 – Model Training**
**Script:** `src/model/train.py`

#### Model Type
**Item-based Collaborative Filtering**

#### Process
1. Build user–item matrix  
2. Compute cosine similarity between movies  
3. Store model artifacts in GCS:

models/v1/
├── item_similarity.parquet
├── movie_index.parquet
└── metadata.json

✅ Model versioning allows future upgrades (v2, v3…).

---

Step 4 – Recommendation Logic**
**Module:** `src/model/recommend.py`

#### Core Logic
- Cold start → return popular movies
- Split ratings:
  - Liked (≥ 4 ⭐)
  - Disliked (≤ 2 ⭐)
- Compute weighted similarity scores
- Penalize disliked movies
- Remove already-rated items
- Rank and return Top-N recommendations

✅ Hybrid logic improves relevance compared to pure popularity.

---

Step 5 – API Layer**
**Module:** `src/api/main.py`

#### Endpoints
- `GET /` → Health check
- `POST /rate` → Store user rating
- `POST /recommend` → Get recommendations

#### Key Components
- `schemas.py` → Request/response validation (Pydantic)
- `store.py` → In-memory session ratings

✅ API is stateless, scalable, and Cloud Run–ready.

---

Step 6 – Streamlit User Interface**
**File:** `streamlit_app.py`

#### Features
- User ID selection
- Live recommendations
- Star-based rating system
- Session + database ratings merge
- Real-time recommendation updates

✅ Makes the project demo-ready and recruiter-friendly.

---

