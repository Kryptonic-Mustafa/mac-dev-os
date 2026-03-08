import os
import time
import subprocess
import shutil
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[💉 M.A.C.DevOS Surgical Sync] {message}...")
    time.sleep(0.5)

def surgical_sync():
    # 1. DELETE CACHED CLIENTS
    print_status("Purging Outdated Client Artifacts")
    paths = [
        PROJECT_PATH / "node_modules/.prisma",
        PROJECT_PATH / "node_modules/@prisma/client"
    ]
    for p in paths:
        if p.exists():
            shutil.rmtree(p)
            print(f"  ✓ Purged: {p}")

    # 2. FORCE GENERATE CLIENT
    # This rebuilds the 'db.review' property into your code
    print_status("Generating Fresh Prisma Client")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # 3. VERIFY SCHEMA SYNC
    print_status("Validating MySQL Schema Alignment")
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)

    print_status("Alignment Complete. RESTART REQUIRED.")

if __name__ == "__main__":
    surgical_sync()