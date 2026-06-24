# Local Monitor Hub

A local Flask dashboard to track personal browsing habits and manage workspace entry points using browser execution logs. Runs entirely offline.

1. Ensure you are on the Main Branch
Make sure you aren't accidentally editing files inside an old, stale feature branch.

Bash
git checkout main


2. Pull Latest Remote Changes (Good Habit)
Even if you are the only developer, always check if your local environment matches your remote repository completely before writing new logic.

Bash
git pull origin main

3. Create a New Feature Branch
Never write new features or trial code directly on your production-ready main branch. Create an isolated branch so your working changes are cleanly grouped.

Bash
git checkout -b feature/domain-grouping-and-filter


Step 1: Save and Commit Your Updates
Run these commands in your terminal to save your feature branch progress:

PowerShell
# 1. Stage your changes
git add app.py templates/index.html

# 2. Commit the updates
git commit -m "feat: add domain grouping, filter app route logging, and rename dashboard"



Step 2: Merge the Code Locally
Since we are keeping it simple on your local machine, merge your feature branch straight into main:

PowerShell
# 1. Flip back to main
git checkout main

# 2. Merge your new grouping updates
git merge feature/domain-grouping-and-filter




pm2 restart edge-monitor