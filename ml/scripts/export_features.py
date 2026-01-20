import requests
import pandas as pd

ES_URL = "http://localhost:9200/filebeat-*/_search"

query = {
    "size": 0,
    "aggs": {
        "logs_per_minute": {
            "date_histogram": {
                "field": "@timestamp",
                "fixed_interval": "1m",
                "min_doc_count": 1
            },
            "aggs": {
                "error_count": {
                    "filter": {"term": {"log.level": "ERROR"}}
                },
                "warn_count": {
                    "filter": {"term": {"log.level": "WARN"}}
                },
                "total_logs": {
                    "value_count": {"field": "log.level"}
                }
            }
        }
    }
}

res = requests.post(ES_URL, json=query).json()

rows = []
for b in res["aggregations"]["logs_per_minute"]["buckets"]:
    if b["total_logs"]["value"] > 0:
        rows.append({
            "timestamp": b["key_as_string"],
            "error_count": b["error_count"]["doc_count"],
            "warn_count": b["warn_count"]["doc_count"],
            "total_logs": b["total_logs"]["value"]
        })

df = pd.DataFrame(rows)
df.to_csv("data/features.csv", index=False)

print("Exported", len(df), "rows to data/features.csv")
