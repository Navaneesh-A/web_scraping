# 📊 Navaneesh Monitor Hub

An automated, local browser telemetry cockpit that securely pulls live Microsoft Edge browsing history files on Windows to analyze productivity distributions, map daily action loops, and generate sequence roadmaps—all running completely locally as a silent background process managed by PM2.

---

## 🚀 Key Architectural Features

* **Data Insulation (Zero Lockups):** Automates background file copying (`shutil`) of the Edge SQLite `History` database file, completely bypassing active browser read-locks.
* **Strict Temporal Filtering:** Self-filters localized dashboard routes (`127.0.0.1`) and groups daily data points strictly bounded by active calendar views.
* **24-Hour Active Map Matrix:** Translates system database epochs into clean, human-readable 12-hour distribution matrices (`AM/PM`).
* **Sequence Learning Roadmaps:** Parses raw chronological interaction flows into interconnected directional nodes ($\rightarrow$) for engineering contexts.
* **Visual Footprints & Micro-Chimes:** Implements cascading slide-animations paired with localized metadata favicons and auditory processing queues on page initialization.

---

## 🛠️ Environment Prerequisites

1. **Python 3.10+** (Added to your local system Environment variables path)
2. **Node.js & NPM** (For global process execution orchestration)
3. **Microsoft Edge Browser** (Running standard profile directories)

---

## 📥 Local Deployment Steps

### 1. File Tree Structure
Ensure your root project layout is mapped exactly like this:
```text
web_scraping/
├── templates/
│   └── index.html
├── app.py
├── PROCESS.md
└── README.md