## Intelligent System Performance Monitoring & Prediction

This project monitors system resource usage (CPU, memory, disk, etc.) and uses machine learning models to detect anomalies and predict future performance.

It is useful for:
- Detecting abnormal system behavior
- Predicting upcoming resource spikes
- Improving system reliability and capacity planning

---

## Features

- Real-time system metrics collection
- Historical data storage and preprocessing
- Machine-learning based performance prediction
- Anomaly / alert detection
- Dashboards for history, insights, and live predictions

---

## Project Structure

- `data/`
	- `raw/system_data.csv` – original collected metrics
	- `processed/clean_data.csv` – cleaned data used for modeling
- `notebooks/`
	- `Preprocessing.ipynb` – data cleaning and feature engineering
	- `train_anomaly.ipynb` – experiments for anomaly detection
	- `test.ipynb` – miscellaneous tests / quick checks
- `src/`
	- `collector.py` – collects live system statistics (CPU, memory, disk, etc.)
	- `db_logger.py` – logs collected metrics to storage/database
	- `train_prediction.py` – trains prediction models on historical data
	- `predict_live.py` – runs trained models on live data
	- `alerts.py` – generates alerts when anomalies or thresholds are detected
	- `dashboard.py` – main dashboard for monitoring
	- `history_dashboard.py` – visualizes historical metrics and trends
	- `insights_dashboard.py` – shows derived insights and analytics
	- `__pycache__/` – Python bytecode cache (ignored by git)

---

## Installation

1. Create and activate a virtual environment (recommended):

	 ```bash
	 python -m venv venv
	 venv\Scripts\activate  # On Windows
	 ```

2. Install dependencies:

	 ```bash
	 pip install -r requirement.txt
	 ```

---

## Usage

Typical ways to run the project (from the project root):

- Collect and log system metrics:

	```bash
	python src/collector.py
	```

- Train prediction models on historical data:

	```bash
	python src/train_prediction.py
	```

- Run live prediction / monitoring:

	```bash
	python src/predict_live.py
	```

- Launch dashboards (depending on how they are implemented in your codebase):

	```bash
	python src/dashboard.py
	```

You can also open the notebooks in `notebooks/` to explore preprocessing and model training interactively.

---

## Technologies

- Python 3.x
- pandas, NumPy
- scikit-learn
- Matplotlib / Seaborn
- psutil (for system monitoring)

---

## Notes

- Make sure your environment has permission to read system metrics.
- For production use, you may want to configure persistent storage (database) in `db_logger.py` and tune alert thresholds in `alerts.py`.

