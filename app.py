import os
import sqlite3
import shutil
from datetime import datetime, timedelta
from flask import Flask, render_template

app = Flask(__name__)

HISTORY_FILE = r"C:\Users\Admin\AppData\Local\Microsoft\Edge\User Data\Default\History"PRODUCTIVE_DOMAINS = ["leetcode.com", "github.com", "codeforces.com", "stackoverflow.com", "gemini.google.com"]

def chrome_time_to_datetime(timestamp):
    try:
        return datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
    except:
        return datetime.now()

def fetch_and_analyze_history():
    if not os.path.exists(HISTORY_FILE):
        return {"error": "History file not found in current directory.", "history": [], "stats": {}}
    
    shutil.copy(HISTORY_FILE, "history_copy.db")
    conn = sqlite3.connect("history_copy.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT url, title, visit_count, last_visit_time 
        FROM urls 
        ORDER BY last_visit_time DESC 
        LIMIT 100
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    parsed_history = []
    daily_counts = {}
    productive_count = 0
    total_count = 0
    
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    weekly_count = 0

    for url, title, count, time_raw in rows:
        visit_date = chrome_time_to_datetime(time_raw)
        date_str = visit_date.strftime("%Y-%m-%d")
        
        daily_counts[date_str] = daily_counts.get(date_str, 0) + count
        total_count += count
        
        if visit_date > one_week_ago:
            weekly_count += count
            
        is_productive = any(domain in url for domain in PRODUCTIVE_DOMAINS)
        if is_productive:
            productive_count += count

        parsed_history.append({
            "url": url,
            "title": title or url,
            "count": count,
            "time": visit_date.strftime("%Y-%m-%d %H:%M:%S"),
            "productive": is_productive
        })

    # Generate 30-day grid matrix data
    calendar_grid = []
    for i in range(29, -1, -1):
        day = now - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        v_count = daily_counts.get(day_str, 0)
        
        if v_count == 0: color = "#1f2937"       # Empty (gray-800)
        elif v_count < 5: color = "#064e3b"     # Low activity (green-900)
        elif v_count < 15: color = "#047857"    # Medium activity (green-700)
        else: color = "#10b981"                 # High activity (green-500)
        
        calendar_grid.append({"date": day_str, "count": v_count, "color": color})

    stats = {
        "today_count": daily_counts.get(now.strftime("%Y-%m-%d"), 0),
        "weekly_count": weekly_count,
        "productive_ratio": round((productive_count / max(total_count, 1)) * 100, 1)
    }

    return {"history": parsed_history[:15], "calendar": calendar_grid, "stats": stats}

@app.route("/")
def index():
    data = fetch_and_analyze_history()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)