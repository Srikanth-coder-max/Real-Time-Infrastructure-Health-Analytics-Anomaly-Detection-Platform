import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="System Insights", layout="wide")
st.title("System Performance Insights")

conn = sqlite3.connect("performance_logs.db")
df = pd.read_sql("SELECT * FROM system_logs", conn)

if df.empty:
    st.warning("No data available yet.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour

total_logs = len(df)
total_anomalies = df["is_anomaly"].sum()
anomaly_rate = (total_anomalies / total_logs) * 100

col1, col2, col3 = st.columns(3)
col1.metric("Total Records", total_logs)
col2.metric("Total Anomalies", int(total_anomalies))
col3.metric("Anomaly Rate (%)", f"{anomaly_rate:.2f}")

st.divider()

st.subheader("Anomalies by Hour of Day")
hourly_anomalies = df.groupby("hour")["is_anomaly"].sum()
st.bar_chart(hourly_anomalies)

st.divider()

st.subheader("Average Resource Usage")
avg_cpu = df["cpu"].mean()
avg_memory = df["memory"].mean()

st.write(f"Average CPU Usage: {avg_cpu:.2f}%")
st.write(f"Average Memory Usage: {avg_memory:.2f}%")

st.divider()

st.subheader("CPU Usage During Anomalies")
st.line_chart(df[df["is_anomaly"] == 1]["cpu"])
