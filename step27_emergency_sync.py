import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚨 M.A.C.DevOS Emergency] {message}...")
    time.sleep(0.5)

def run_emergency_sync():
    # 1. HARD PURGE OF CACHED CLIENTS
    print_status("Purging Outdated Prisma Artifacts")
    # This removes the hidden .prisma folder that often holds old schema versions
    subprocess.run("rmdir /s /q node_modules\\.prisma", shell=True, cwd=PROJECT_PATH)
    
    # 2. FORCE SYNC SCHEMA TO MYSQL
    print_status("Synchronizing Matrix Schema with MySQL")
    # This physically creates the 'Review' and 'SystemSettings' tables in your DB
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    
    # 3. REGENERATE CLIENT
    print_status("Generating Fresh Telemetry Client")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    print_status("System alignment complete. RESTART YOUR TERMINAL NOW.")

if __name__ == "__main__":
    run_emergency_sync()