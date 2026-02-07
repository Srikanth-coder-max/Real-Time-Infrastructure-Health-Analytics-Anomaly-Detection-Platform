import sqlite3
from datetime import datetime
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent.parent / "performance_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS system_logs (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    cpu REAL,
                    memory REAL,
                    is_anomaly INTEGER
                   )
    """)
    conn.commit()
    conn.close()

def log_metrics(cpu, memory, is_anomaly):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO system_logs (timestamp, cpu, memory, is_anomaly)
        VALUES (?, ?, ?, ?)
    """, (datetime.now(), cpu, memory, is_anomaly))

    conn.commit()
    conn.close()

    
    
