import os
import sqlite3
import shutil
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)

HISTORY_FILE = r"C:\Users\Admin\AppData\Local\Microsoft\Edge\User Data\Default\History"
LOCAL_COPY = "history_live_copy.db"
ARCHIVE_LOG = "hourly_archive.json"

PRODUCTIVE_DOMAINS = ["leetcode.com", "github.com", "codeforces.com", "stackoverflow.com", "gemini.google.com"]

def chrome_time_to_datetime(timestamp):
    try:
        return datetime(1601, 1, 1) + timedelta(microseconds=timestamp)
    except:
        return datetime.now()

def load_archive():
    if os.path.exists(ARCHIVE_LOG):
        with open(ARCHIVE_LOG, 'r') as f:
            return json.load(f)
    return {}

def save_archive(data):
    with open(ARCHIVE_LOG, 'w') as f:
        json.dump(data, f, indent=4)

def update_hourly_archive(rows):
    archive = load_archive()
    for url, title, count, time_raw in rows:
        if "127.0.0.1:5000" in url or "localhost:5000" in url:
            continue
        visit_date = chrome_time_to_datetime(time_raw)
        if visit_date < datetime(2026, 6, 24):
            continue
            
        date_str = visit_date.strftime("%Y-%m-%d")
        hour_str = str(visit_date.hour)
        
        if date_str not in archive:
            archive[date_str] = {str(h): 0 for h in range(24)}
        
        archive[date_str][hour_str] = archive[date_str].get(hour_str, 0) + 1
    save_archive(archive)

def fetch_and_analyze_history(target_date_str):
    if not os.path.exists(HISTORY_FILE):
        return {"error": "Live tracking unverified.", "history": [], "grouped_history": [], "calendar": [], "hourly_map": [], "roadmap": [], "stats": {}}
    
    try:
        shutil.copy2(HISTORY_FILE, LOCAL_COPY)
        conn = sqlite3.connect(LOCAL_COPY)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 500")
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        return {"error": str(e), "history": [], "grouped_history": [], "calendar": [], "hourly_map": [], "roadmap": [], "stats": {}}

    update_hourly_archive(rows)
    archive = load_archive()

    parsed_history = []
    domain_groups = {}
    daily_counts = {}
    roadmap_nodes = []
    productive_count, total_count, weekly_count = 0, 0, 0
    
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)

    for url, title, count, time_raw in rows:
        # 🛑 Block both old 5000 and new 5500 local dashboard urls
        if "127.0.0.1" in url or "localhost" in url:
            continue

        visit_date = chrome_time_to_datetime(time_raw)
        date_str = visit_date.strftime("%Y-%m-%d")
        
        # Track historical rolling dates for the 30-day index
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        if visit_date > one_week_ago:
            weekly_count += 1

        # 🎯 CRITICAL: ONLY aggregate metrics and list items if they belong to the selected date view
        if date_str == target_date_str:
            domain = urlparse(url).netloc or "Other"
            domain_groups[domain] = domain_groups.get(domain, 0) + 1
            total_count += 1
            
            is_productive = any(dm in url for dm in PRODUCTIVE_DOMAINS)
            if is_productive:
                productive_count += 1
                if len(roadmap_nodes) < 5 and title:
                    roadmap_nodes.append({"title": title[:35] + "...", "url": url, "domain": domain})

            parsed_history.append({
                "url": url,
                "title": title or url,
                "count": 1,
                "time": visit_date.strftime("%I:%M %p"),
                "domain": domain,
                "productive": is_productive
            })

    # Format 24-Hour Timeline using clear 12-Hour Labels (AM/PM)
    target_hours = archive.get(target_date_str, {str(h): 0 for h in range(24)})
    hourly_map = []
    for h in range(24):
        h_count = target_hours.get(str(h), 0)
        
        # Calculate human 12-hour string marker
        if h == 0: label = "12 AM"
        elif h == 12: label = "12 PM"
        elif h > 12: label = f"{h-12} PM"
        else: label = f"{h} AM"
        
        color = "#1f2937" if h_count == 0 else "#064e3b" if h_count < 3 else "#047857" if h_count < 8 else "#10b981"
        hourly_map.append({"hour_label": label, "count": h_count, "color": color})

    calendar_grid = []
    for i in range(29, -1, -1):
        day = now - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        v_count = daily_counts.get(day_str, 0)
        color = "#1f2937" if v_count == 0 else "#064e3b" if v_count < 5 else "#047857" if v_count < 15 else "#10b981"
        calendar_grid.append({"date": day_str, "count": v_count, "color": color})

    stats = {
        "today_count": total_count,
        "weekly_count": weekly_count,
        "productive_ratio": round((productive_count / max(total_count, 1)) * 100, 1)
    }

    return {
        "history": parsed_history[:10],
        "grouped_history": [{"domain": k, "count": v} for k, v in sorted(domain_groups.items(), key=lambda x: x[1], reverse=True)[:5]],
        "calendar": calendar_grid,
        "hourly_map": hourly_map,
        "roadmap": list(reversed(roadmap_nodes)),
        "stats": stats
    }

@app.route("/")
def index():
    current_date_obj = datetime.now()
    date_param = request.args.get("date", current_date_obj.strftime("%Y-%m-%d"))
    
    # Calculate stepping dates for arrows
    try:
        selected_dt = datetime.strptime(date_param, "%Y-%m-%d")
    except:
        selected_dt = current_date_obj
        date_param = selected_dt.strftime("%Y-%m-%d")
        
    prev_date = (selected_dt - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (selected_dt + timedelta(days=1)).strftime("%Y-%m-%d")
    
    data = fetch_and_analyze_history(date_param)
    return render_template("index.html", data=data, selected_date=date_param, prev_date=prev_date, next_date=next_date)

if __name__ == "__main__":
    app.run(debug=False, port=5500)