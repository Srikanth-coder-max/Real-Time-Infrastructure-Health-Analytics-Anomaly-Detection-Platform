import psutil
import joblib
import time
import pandas as pd
from db_logger import init_db, log_metrics

model = joblib.load("models/anomaly_model.pkl")
init_db()

print("Real Time monitoring has beed started....Press ctrl+c to exit")

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    cpu_scaled = cpu/100
    memory_scaled = memory/100

    X = pd.DataFrame([[cpu_scaled, memory_scaled]], columns=[
                     "cpu_scaled", "memory_scaled"])

    prediction = model.predict(X)[0]

    is_anomaly = int(prediction==-1)
    log_metrics(cpu, memory, is_anomaly)

    if prediction == -1:
        print(f"Anomaly Detected | CPU:{cpu:.1f}% | Memory:{memory:.1f}%")
    else:
        print(f"Normal | CPU:{cpu:.1f}% | Memory:{memory:.1f}%")

    time.sleep(1)
