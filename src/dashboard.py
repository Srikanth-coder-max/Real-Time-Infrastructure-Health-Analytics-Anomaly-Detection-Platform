import streamlit as st
import psutil
import time
import joblib
import pandas as pd

model = joblib.load("models/anomaly_model.pkl")

st.set_page_config(page_title="System Performance Dashboard", page_icon="📈", layout="wide")
st.title("📈 System Performance Monitor")
st.caption("Real-time CPU and memory monitoring with anomaly detection")

with st.sidebar:
    st.header("Controls")
    max_points = st.slider("History length", min_value=30, max_value=600, value=120, step=10)

if "cpu_history" not in st.session_state:
    st.session_state.cpu_history = []
    st.session_state.memory_history = []
    st.session_state.time_history = []

cpu = psutil.cpu_percent(interval=1)
memory = psutil.virtual_memory().percent

cpu_scaled = cpu / 100
memory_scaled = memory / 100

X = pd.DataFrame([[cpu_scaled, memory_scaled]], columns=["cpu_scaled", "memory_scaled"])
prediction = model.predict(X)[0]

st.session_state.cpu_history.append(cpu)
st.session_state.memory_history.append(memory)
st.session_state.time_history.append(time.strftime("%H:%M:%S"))

if len(st.session_state.cpu_history) > max_points:
    st.session_state.cpu_history = st.session_state.cpu_history[-max_points:]
    st.session_state.memory_history = st.session_state.memory_history[-max_points:]
    st.session_state.time_history = st.session_state.time_history[-max_points:]

col1, col2, col3 = st.columns(3)
col1.metric("CPU", f"{cpu:.1f}%")
col2.metric("Memory", f"{memory:.1f}%")
col3.metric("Status", "Anomaly" if prediction == -1 else "Normal")

st.subheader("Usage Trends")
chart_df = pd.DataFrame(
    {
        "CPU %": st.session_state.cpu_history,
        "Memory %": st.session_state.memory_history,
    },
    index=st.session_state.time_history,
)
st.line_chart(chart_df)

if prediction == -1:
    st.error(f"⚠️ Anomaly Detected | CPU {cpu:.1f}% | Memory {memory:.1f}%")
else:
    st.success(f"Normal | CPU {cpu:.1f}% | Memory {memory:.1f}%")

st.caption(f"Last update: {st.session_state.time_history[-1]}")

time.sleep(1)

st.rerun()
