import sqlite3
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Load historical data
conn = sqlite3.connect("performance_logs.db")
df = pd.read_sql("SELECT * FROM system_logs ORDER BY timestamp", conn)

df["cpu_next"] = df["cpu"].shift(-1)
df.dropna(inplace=True)

X = df[["cpu", "memory"]]
y = df["cpu_next"]

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "models/cpu_prediction_model.pkl")

print("CPU prediction model trained & saved!")
