import pandas as pd
import requests

df = pd.read_csv("data/anomaly_results.csv")

ES_URL = "http://localhost:9200/anomaly-results/_doc"

for _, row in df.iterrows():
    doc = {
        "timestamp": row["timestamp"],
        "error_count": int(row["error_count"]),
        "warn_count": int(row["warn_count"]),
        "total_logs": int(row["total_logs"]),
        "anomaly": int(row["anomaly"]),
        "anomaly_score": float(row["anomaly_score"])
    }
    requests.post(ES_URL, json=doc)

print("Anomaly results pushed to Elasticsearch")
