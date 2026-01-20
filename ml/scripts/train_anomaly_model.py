import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("data/features.csv")

X = df[["error_count", "warn_count", "total_logs"]]

model = IsolationForest(
    n_estimators=100,
    contamination=0.15,
    random_state=42
)

df["anomaly"] = model.fit_predict(X)
df["anomaly_score"] = model.decision_function(X)

df.to_csv("data/anomaly_results.csv", index=False)

print("Anomaly detection complete")
print(df)
