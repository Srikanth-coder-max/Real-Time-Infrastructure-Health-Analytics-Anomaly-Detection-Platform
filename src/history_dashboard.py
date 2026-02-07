import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="System History", page_icon="🧭", layout="wide")
st.title("🧭 System Performance History")
st.caption("Historical CPU and memory trends with anomaly markers")

db_path = Path(__file__).resolve().parent.parent / "performance_logs.db"
conn = sqlite3.connect(db_path)
conn.execute("""
    CREATE TABLE IF NOT EXISTS system_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        cpu REAL,
        memory REAL,
        is_anomaly INTEGER
    )
""")

df = pd.read_sql("SELECT * FROM system_logs ORDER BY timestamp", conn)

if df.empty:
    st.info("No data yet. Run alerts.py to generate logs.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date

with st.sidebar:
    st.header("Filters")
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    show_anomalies = st.toggle("Highlight anomalies", value=True)
    show_table = st.checkbox("Show recent logs", value=False)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    df = df.loc[mask]

total_rows = len(df)
anomaly_count = int(df["is_anomaly"].sum())
latest_cpu = df.iloc[-1]["cpu"]
latest_mem = df.iloc[-1]["memory"]
anomaly_rate = (anomaly_count / total_rows) * 100 if total_rows else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU (latest)", f"{latest_cpu:.1f}%")
col2.metric("Memory (latest)", f"{latest_mem:.1f}%")
col3.metric("Total samples", f"{total_rows}")
col4.metric("Anomaly rate", f"{anomaly_rate:.1f}%")

tab_cpu, tab_mem = st.tabs(["CPU Trend", "Memory Trend"])

with tab_cpu:
    fig1, ax1 = plt.subplots(figsize=(12, 2.8))
    ax1.plot(df["timestamp"], df["cpu"], color="#1f77b4", linewidth=1.8)
    if show_anomalies:
        ax1.scatter(
            df[df["is_anomaly"] == 1]["timestamp"],
            df[df["is_anomaly"] == 1]["cpu"],
            color="#d62728",
            s=45,
            label="Anomaly",
        )
        ax1.legend(loc="upper right")
    ax1.set_ylabel("CPU %")
    ax1.grid(alpha=0.3)
    st.pyplot(fig1, use_container_width=True)

with tab_mem:
    fig2, ax2 = plt.subplots(figsize=(12, 2.8))
    ax2.plot(df["timestamp"], df["memory"], color="#2ca02c", linewidth=1.8)
    if show_anomalies:
        ax2.scatter(
            df[df["is_anomaly"] == 1]["timestamp"],
            df[df["is_anomaly"] == 1]["memory"],
            color="#d62728",
            s=45,
            label="Anomaly",
        )
        ax2.legend(loc="upper right")
    ax2.set_ylabel("Memory %")
    ax2.grid(alpha=0.3)
    st.pyplot(fig2, use_container_width=True)

if show_table:
    st.subheader("Recent logs")
    st.dataframe(df.tail(50).sort_values("timestamp", ascending=False), use_container_width=True)
