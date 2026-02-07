import psutil
import pandas as pd
from datetime import datetime
import time
from pathlib import Path

DATA_PATH = Path('data/raw/system_data.csv')


def collect_metrics():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    records = []

    print("Collecting System data. To stop press ctrl+c")

    try:
        while True:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent

            timestamp = datetime.now()

            records.append(
                {
                    "timeStamp": timestamp,
                    "CPU_Usage": cpu_usage,
                    "Memory_Usage" : memory_usage
                }
            )
    except KeyboardInterrupt:
        df = pd.DataFrame(records)
        df.to_csv(DATA_PATH, index=False)
        print(f"\n Saved data to {DATA_PATH}")

if __name__ == "__main__":
    collect_metrics()

