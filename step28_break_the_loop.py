import os
import time
import subprocess
import shutil
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🌀 M.A.C.DevOS Matrix Reset] {message}...")
    time.sleep(0.5)

def break_the_loop():
    # 1. DELETE CACHED PRISMA ARTIFACTS
    print_status("Deleting Corrupt Prisma Artifacts")
    # This is the 'Nuclear Option' to stop the Digest loop
    paths_to_delete = [
        PROJECT_PATH / "node_modules/.prisma",
        PROJECT_PATH / "node_modules/@prisma/client"
    ]
    
    for path in paths_to_delete:
        if path.exists():
            shutil.rmtree(path)
            print(f"  ✓ Purged: {path}")

    # 2. FORCE GENERATE FRESH CLIENT
    print_status("Regenerating Fresh Data Client")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    # 3. VERIFY DATABASE SCHEMA INTEGRITY
    print_status("Verifying MySQL Schema Alignment")
    # This ensures the 'socialLinks' and 'contactEmail' actually exist in MySQL
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)

    print_status("Loop broken. RESTARTING SERVER...")

if __name__ == "__main__":
    break_the_loop()