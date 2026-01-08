📂 Project Structure
GCP_movie_recommendation_project/
│
├── data/
│   ├── raw/                  # Raw datasets (movies, ratings, metadata)
│   ├── processed/            # Cleaned & feature-engineered data
│
├── notebooks/
│   ├── exploration.ipynb     # Data exploration & EDA
│   ├── feature_engineering.ipynb
│   └── model_training.ipynb
│
├── src/
│   ├── data_ingestion/
│   │   └── load_to_gcs.py    # Upload data to Cloud Storage
│   │
│   ├── bigquery/
│   │   └── load_to_bq.py     # Load & transform data in BigQuery
│   │
│   ├── training/
│   │   └── train_model.py    # Train recommendation model (Vertex AI)
│   │
│   ├── inference/
│   │   └── predict.py        # Prediction logic
│   │
│   └── api/
│       └── main.py           # FastAPI app (Cloud Run)
│
├── Dockerfile                # Containerization for Cloud Run
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore


🔄 End-to-End Workflow :

1️⃣ Data Ingestion (Cloud Storage)
Raw movie and rating datasets are uploaded to Google Cloud Storage
This acts as the Bronze layer (raw, immutable data)

2️⃣ Data Processing & Analytics (BigQuery)
Data is loaded from GCS into BigQuery
Cleaning, joins, and aggregations are done using SQL
Feature tables are created:
    User–Movie interactions
    Rating statistics
    Popularity metrics

3️⃣ Feature Engineering
Transform raw ratings into ML-ready features:
    User vectors
    Movie vectors
    Interaction matrices

4️⃣ Model Training (Vertex AI)
A recommendation model is trained using Vertex AI
Supports scalable training without managing infrastructure
Model artifacts are stored and versioned
ML Logic (Typical):
    Collaborative Filtering
    Similarity-based recommendations
    User-item interaction modeling

5️⃣ Model Deployment (Cloud Run)
Model is wrapped inside a FastAPI application
Containerized using Docker
Deployed on Cloud Run for:
    Auto-scaling
    Cost efficiency
    HTTP API access

6️⃣ Inference & Recommendation API
API endpoints allow:
    Requesting movie recommendations for a user
    Fetching similar movies
Cloud Run communicates with:
    Vertex AI for predictions
    BigQuery for metadata

7️⃣ Frontend User Interface (Streamlit)
A Streamlit web application is created to provide a simple and interactive user interface.
The UI allows users to:
    Select or enter a user ID
    Request personalized movie recommendations
    Explore similar movies based on a selected title
Streamlit communicates with:
    Cloud Run API to fetch real-time recommendations
    Vertex AI indirectly for model inference
    BigQuery indirectly for movie metadata and details
