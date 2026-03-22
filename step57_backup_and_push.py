import os
import time
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[📦 M.A.C.DevOS Version Control] {message}")
    time.sleep(0.5)

def run_git_command(command, error_message):
    try:
        # Run the command and wait for it to finish
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  --> Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {error_message}")
        print(f"Details: {e.stderr.strip()}")
        return False

def create_local_backup():
    # Create a timestamp for the zip file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"mac-dev-os_backup_{timestamp}.zip"
    
    print_status(f"Creating local snapshot: {zip_filename}...")
    
    # Folders we DO NOT want to zip (they are huge and can be regenerated)
    ignore_dirs = {'.git', 'node_modules', '.next', '.vercel', '__pycache__'}
    
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(PROJECT_PATH):
                # Tell os.walk to skip our ignored directories
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                for file in files:
                    # Prevent the script from zipping the zip file it's currently creating
                    if not file.endswith('.zip'):
                        file_path = os.path.join(root, file)
                        # Calculate the relative path so the zip structure is clean
                        arcname = os.path.relpath(file_path, PROJECT_PATH)
                        zipf.write(file_path, arcname)
                        
        print(f"  --> Backup compressed and saved securely.")
        return zip_filename
    except Exception as e:
        print(f"\n[ERROR] Failed to create zip file: {e}")
        return None

def main():
    print("====================================================")
    print("      INITIATING BACKUP & DEPLOYMENT PROTOCOL       ")
    print("====================================================")

    # PHASE 1: PULL
    print_status("Phase 1: Syncing with remote repository (git pull)")
    if not run_git_command("git pull origin main", "Failed to pull from remote. You may have merge conflicts."):
        print("\n[!] Aborting deployment due to pull failure. Please resolve conflicts manually.")
        return

    # PHASE 2: ZIP BACKUP
    print_status("Phase 2: Compressing local Matrix (Excluding node_modules/.next)")
    backup_file = create_local_backup()
    if not backup_file:
        print("\n[!] Aborting deployment due to backup failure.")
        return

    # PHASE 3: PUSH
    print_status("Phase 3: Preparing new payload for deployment (git add/commit/push)")
    
    # Automatically generate a commit message based on the time
    commit_time = datetime.now().strftime("%I:%M %p, %b %d")
    commit_msg = f"AUTO-DEPLOY: Routine sync and update at {commit_time}"
    
    if run_git_command("git add .", "Failed to stage files."):
        if run_git_command(f'git commit -m "{commit_msg}"', "Failed to commit files. (Are there no changes to commit?)"):
            if run_git_command("git push origin main", "Failed to push to remote."):
                print("\n====================================================")
                print(" [SUCCESS] M.A.C.DevOS Matrix Successfully Deployed! ")
                print(f" [BACKUP]  Local safety snapshot: {backup_file}")
                print("====================================================")
            else:
                print("\n[!] Failed to push to remote. Check your internet or GitHub permissions.")

if __name__ == "__main__":
    main()