import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔄 M.A.C.DevOS Pipeline Upgrade] {message}...")
    time.sleep(0.5)

def upgrade_master_script():
    print_status("Rewriting step57_backup_and_push.py to use the 'from_server' vault")
    step57_path = PROJECT_PATH / "step57_backup_and_push.py"
    
    new_step57_content = """import os
import time
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

PROJECT_PATH = Path.cwd()
# Define the new secure vault directory
VAULT_DIR = PROJECT_PATH / "from_server"

def print_status(message):
    print(f"\\n[📦 M.A.C.DevOS Version Control] {message}")
    time.sleep(0.5)

def run_git_command(command, error_message):
    try:
        subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  --> Success: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\\n[ERROR] {error_message}\\nDetails: {e.stderr.strip()}")
        return False

def create_local_backup():
    # Ensure the vault directory exists
    if not VAULT_DIR.exists():
        VAULT_DIR.mkdir()
        print(f"  --> Created new secure vault: {VAULT_DIR.name}/")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = VAULT_DIR / f"mac-dev-os_sync_{timestamp}.zip"
    
    # Ignore heavy folders and backup vaults
    ignore_dirs = {'.git', 'node_modules', '.next', '.vercel', '__pycache__', 'bkp', 'from_server'}
    
    print_status(f"Compressing current Matrix into: from_server/{zip_filename.name}...")
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(PROJECT_PATH):
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                for file in files:
                    if not file.endswith('.zip'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, PROJECT_PATH)
                        zipf.write(file_path, arcname)
        print(f"  --> Backup compressed and saved securely in /from_server.")
        return zip_filename
    except Exception as e:
        print(f"\\n[ERROR] Failed to create zip file: {e}")
        return None

def main():
    print("====================================================")
    print("      INITIATING BACKUP & DEPLOYMENT PROTOCOL       ")
    print("====================================================")
    
    print_status("Phase 1: Syncing with remote repository (git pull)")
    if not run_git_command("git pull origin main", "Failed to pull from remote."): return

    print_status("Phase 2: Compressing local Matrix to Vault")
    backup_file = create_local_backup()
    if not backup_file: return

    print_status("Phase 3: Preparing new payload for deployment (git push)")
    commit_time = datetime.now().strftime("%I:%M %p, %b %d")
    commit_msg = f"AUTO-DEPLOY: Routine sync and secure vault backup at {commit_time}"
    
    if run_git_command("git add .", "Failed to stage files."):
        if run_git_command(f'git commit -m "{commit_msg}"', "Failed to commit files."):
            if run_git_command("git push origin main", "Failed to push to remote."):
                print("\\n====================================================")
                print(" [SUCCESS] M.A.C.DevOS Matrix Successfully Deployed! ")
                print("====================================================")

if __name__ == "__main__":
    main()
"""
    with open(step57_path, "w", encoding="utf-8") as f:
        f.write(new_step57_content)

def upgrade_script_log():
    print_status("Updating script.txt to reflect the new architecture")
    script_txt_path = PROJECT_PATH / "script.txt"
    
    log_content = f"""====================================================
      M.A.C.DevOS ESSENTIAL AUTOMATION SCRIPTS      
====================================================
Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

----------------------------------------------------
SCRIPT 1: MASTER DEPLOY & BACKUP (step57_backup_and_push.py)
Description: Syncs with Git, zips a backup into the /from_server vault, and pushes to Vercel.
----------------------------------------------------
(See step57_backup_and_push.py for active code)

----------------------------------------------------
SCRIPT 2: THE SYSTEM SCANNER (generate_system_overview.py)
Description: Crawls your project and generates system.txt for AI context.
----------------------------------------------------
(See generate_system_overview.py for active code)
"""
    with open(script_txt_path, "w", encoding="utf-8") as f:
        f.write(log_content)

if __name__ == "__main__":
    upgrade_master_script()
    upgrade_script_log()
    print("\n[SUCCESS] Pipeline upgraded! Your backups will now safely route to /from_server.")