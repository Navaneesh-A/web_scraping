import sqlite3
import shutil
import os
from datetime import datetime, timedelta

# ✅ Use History file from current directory
history_file = "History"

if not os.path.exists(history_file):
    print(f"Error: {history_file} file not found in current directory")
    exit(1)

shutil.copy(history_file, "history_copy.db")

conn = sqlite3.connect("history_copy.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT url, title, visit_count, last_visit_time
    FROM urls
    ORDER BY last_visit_time DESC
    LIMIT 20
""")

def chrome_time(timestamp):
    return datetime(1601, 1, 1) + timedelta(microseconds=timestamp)

for url, title, count, time in cursor.fetchall():
    print(f"URL        : {url}")
    print(f"Title      : {title}")
    print(f"Visits     : {count}")
    print(f"Last Visit : {chrome_time(time)}")
    print("-" * 60)

conn.close()