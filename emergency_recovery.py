import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🚨 M.A.C.DevOS Recovery] {message}...")
    time.sleep(0.5)

def run_recovery():
    # 1. DELETE OLD CLIENT
    print_status("Purging Corrupt Prisma Client")
    client_path = PROJECT_PATH / "node_modules/.prisma"
    if client_path.exists():
        import shutil
        shutil.rmtree(client_path)
    
    # 2. FORCE SYNC & GENERATE
    print_status("Synchronizing Schema with MySQL Workbench")
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)
    
    print_status("Regenerating Fresh Prisma Client")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    print_status("Recovery sequence complete. Please restart your server.")

if __name__ == "__main__":
    run_recovery()