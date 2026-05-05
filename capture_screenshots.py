import time
import subprocess
from PIL import ImageGrab
import os
import sys

# Set UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Wait for app to be ready
time.sleep(3)

# Screenshot each dashboard
dashboards = [
    ("earth-pulse", "screenshots/earth-pulse.png"),
    ("market", "screenshots/market.png"),
    ("ai-signals", "screenshots/ai-signals.png"),
    ("geo-map", "screenshots/geo-map.png"),
]

# Create screenshots directory
os.makedirs("screenshots", exist_ok=True)

for dashboard, filename in dashboards:
    url = f"http://localhost:3000/{dashboard}"
    print(f"Capturing {dashboard}...", flush=True)

    # Open in default browser
    subprocess.Popen(f'start msedge "{url}"', shell=True)

    # Wait for page to load
    time.sleep(4)

    # Take screenshot
    screenshot = ImageGrab.grab()
    screenshot.save(filename)
    print(f"Saved {filename}", flush=True)

    # Close browser tab
    subprocess.Popen("taskkill /f /im msedge.exe", shell=True)
    time.sleep(1)

print("\nAll screenshots captured!")
