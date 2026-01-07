from google.cloud import bigquery
from google.cloud import storage

print("=== SANITY CHECK START ===")

# ---- BigQuery check ----
print("\n[1] Checking BigQuery access...")
bq_client = bigquery.Client()

datasets = list(bq_client.list_datasets())
print(f"✔ BigQuery OK - {len(datasets)} datasets accessible")

# Print first few dataset names
for ds in datasets[:5]:
    print(" -", ds.dataset_id)

# ---- Cloud Storage check ----
print("\n[2] Checking Cloud Storage access...")
gcs_client = storage.Client()

buckets = list(gcs_client.list_buckets())
print(f"✔ Cloud Storage OK - {len(buckets)} buckets accessible")

# Print first few bucket names
for b in buckets[:5]:
    print(" -", b.name)

print("\n=== SANITY CHECK PASSED ===")
