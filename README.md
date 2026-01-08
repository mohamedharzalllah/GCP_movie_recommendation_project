PROJECT OVERVIEW

This project is an end-to-end Movie Recommendation System designed to demonstrate how to build, train, and serve a machine learning model using Google Cloud Platform (GCP).

The goal is to show:

How cloud storage is used to manage data and model artifacts

How machine learning pipelines are structured step by step

How recommendations can be exposed via an API or UI

How a real user can interact with the system

The system recommends movies based on:

User historical ratings (personalized recommendations)

Movie-to-movie similarity (item-based collaborative filtering)

Global popularity for new users (cold start)

GLOBAL ARCHITECTURE (GCP-CENTERED)

Google Cloud Storage (GCS)

Central storage for:

Raw data

Curated datasets

Trained model artifacts

Feature files (popular movies)

Google Cloud Compute (Vertex AI Workbench / VM)

Runs Python scripts

Trains the ML model

Hosts Streamlit and FastAPI services

Optional Google BigQuery

Original data source for ratings and movies

Used during extraction step

PROJECT STRUCTURE

Movie_Recommendation_System/

src/
data/ -> GCP data access (GCS, BigQuery)
model/ -> Training & recommendation logic
api/ -> FastAPI service (optional)

scripts/ -> Step-by-step execution scripts
notebooks/ -> Exploration and experiments
infra/ -> Infrastructure-related configs

streamlit_app.py
requirements.txt
Dockerfile
README.txt

STEP-BY-STEP PIPELINE WITH GCP USAGE
STEP 0 — PROJECT SKELETON

Purpose:

Create a clean and scalable project structure

GCP Usage:

None directly

This step prepares the project to be executed on a GCP VM or Vertex AI Workbench

Why it matters:

Clean structure is essential for cloud-based projects

Makes collaboration and deployment easier

STEP 1 — GCS IO UTILITIES

Files:

src/data/gcs_io.py

Purpose:

Centralize all communication with Google Cloud Storage (GCS)

GCP Usage:

Uses the GCS Python SDK

Authenticates automatically via the GCP environment

Reads and writes Parquet files directly from/to a GCS bucket

Why it matters:

Decouples code from storage

Makes it easy to move from local to cloud environments

Enables scalable data and model storage

STEP 2 — DATA EXTRACTION (BIGQUERY → GCS)

Files:

src/data/bq_reader.py

scripts/01_extract_bq_to_gcs.py

Purpose:

Extract raw data from BigQuery (or another source)

Store it in GCS as raw datasets

GCP Usage:

BigQuery is used as the data warehouse

Data is exported to GCS buckets

GCS becomes the single source of truth for downstream steps

Why it matters:

Separates data ingestion from data processing

Reduces repeated BigQuery queries (cost-efficient)

Enables batch processing

STEP 3 — CURATED DATA + POPULAR MOVIES

Files:

scripts/02_build_curated.py

src/data/* helpers

Purpose:

Clean raw datasets

Build curated datasets for modeling

Compute popular movies for cold-start recommendations

GCP Usage:

Reads raw data from GCS

Writes curated Parquet files back to GCS

Writes popular_movies.json to GCS

Why it matters:

GCS acts as a data lake

Curated layer improves data quality

Popular movies feature supports users with no history

STEP 4 — MODEL TRAINING (ITEM-BASED CF)

Files:

src/model/train.py

scripts/03_train_model.py

Purpose:

Train an item-based collaborative filtering model

Compute movie-to-movie similarity

GCP Usage:

Training runs on a GCP VM / Vertex AI Workbench

Reads curated datasets from GCS

Writes trained model artifacts to GCS:

item_similarity.parquet

movie_index.parquet

metadata.json

Why it matters:

GCS stores versioned model artifacts

Training is reproducible

No local dependency on model files

STEP 5 — RECOMMENDER SERVICE

Files:

src/model/recommend.py

scripts/04_test_recommender.py

Purpose:

Load trained artifacts from GCS

Generate recommendations for users

GCP Usage:

Reads model artifacts directly from GCS

Does not store anything locally

Uses GCS as a model registry

Recommendation logic:

If user has no ratings → return popular movies

If user has ratings:

Boost movies similar to highly-rated movies

Penalize movies similar to low-rated movies

Exclude already-rated movies

Why it matters:

Cloud-native inference

Easy to deploy as API or UI backend

STEP 6 — FASTAPI SERVICE (OPTIONAL)

Files:

src/api/main.py

Purpose:

Expose recommendations as a REST API

GCP Usage:

Runs on a GCP VM

Can be containerized and deployed later

Uses GCS for model loading

Why it matters:

Enables microservice architecture

Ready for cloud deployment (Cloud Run / GKE)

STEP 7 — STREAMLIT FRONTEND

Files:

streamlit_app.py

Purpose:

Interactive UI for users

Rate movies

See recommendations update in real time

GCP Usage:

Runs on GCP VM / Vertex AI Workbench

Reads recommendations via RecommenderService

Loads data and models from GCS

User features:

Enter a user ID

View recommended movies

Rate movies (1–5 stars)

See already-rated movies

Recommendations update dynamically

STEP 8 — NGROK + ACCESS

Purpose:

Make Streamlit accessible outside GCP

GCP Usage:

Streamlit runs inside GCP

ngrok creates a secure public tunnel to the VM

Why it matters:

Enables demos

Enables external access without deployment permissions

WHY GCP IS CENTRAL TO THIS PROJECT

Google Cloud Platform is used as:

Data lake (GCS)

Model registry (GCS)

Compute environment (VM / Vertex AI Workbench)

Optional data warehouse (BigQuery)

Hosting platform (Streamlit / FastAPI)

This mirrors real-world ML production pipelines.

KEY SKILLS DEMONSTRATED

Cloud-native ML development

Data engineering on GCP

Collaborative filtering models

Model versioning in cloud storage

API and UI integration

Clean Git and project structure



lien Swagger :https://101cd6cec241bca7-dot-europe-west1.notebooks.googleusercontent.com/proxy/8000/docs