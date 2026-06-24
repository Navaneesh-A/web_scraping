cat << 'EOF' > PROCESS.md
# 🔄 PM2 Process Management

Use these commands to manage your background Flask server locally using PM2.

### 1. First-Time Setup
If you haven't configured PM2 for this project yet, run:
```bash
# Install PM2 globally
npm install pm2 -g

# Start the Flask app as a background service
pm2 start app.py --name "edge-monitor" --interpreter python

# Save the process so it boots automatically with your laptop
pm2 save


Now you have access to your exact preferred commands:

Check status: pm2 status

View live terminal logs: pm2 logs edge-monitor

Stop the app instantly: pm2 stop edge-monitor


npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.17.0
npm notice To update run: npm install -g npm@11.17.0
npm notice
PS C:\Users\Admin\Desktop\hmm\history\web_scraping> pm2 start app.py --name "edge-monitor" --interpreter python
[PM2] Starting C:\Users\Admin\Desktop\hmm\history\web_scraping\app.py in fork_mode (1 instance)
[PM2] Done.
┌────┬────────────────────┬──────────┬──────┬───────────┬──────────┬──────────┐
│ id │ name               │ mode     │ ↺    │ status    │ cpu      │ memory   │
├────┼────────────────────┼──────────┼──────┼───────────┼──────────┼──────────┤
│ 1  │ edge-monitor       │ fork     │ 0    │ online    │ 0%       │ 41.3mb   │
│ 0  │ my-app             │ fork     │ 0    │ online    │ 0%       │ 21.5mb   │
└────┴────────────────────┴──────────┴──────┴───────────┴──────────┴──────────┘


