import psutil
import time
import joblib
import pandas as pd

model = joblib.load("models/cpu_prediction_model.pkl")

print("Live CPU prediction started...\n")

while True:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    X = pd.DataFrame([[cpu, memory]], columns=["cpu", "memory"])

    predicted_cpu = model.predict(X)[0]

    print(f"Current CPU: {cpu:.1f}% | Predicted next: {predicted_cpu:.1f}%")

    if predicted_cpu > 80:
        print("High CPU spike predicted soon!")

    time.sleep(1)
