import os
import zipfile
import time
from datetime import datetime
from pathlib import Path

PROJECT_PATH = Path.cwd()
BKP_DIR = PROJECT_PATH / "bkp"

def print_status(message):
    print(f"\n[🔐 M.A.C.DevOS Vault] {message}...")
    time.sleep(0.5)

def create_vault_and_backup():
    # 1. Ensure 'bkp' directory exists
    if not BKP_DIR.exists():
        BKP_DIR.mkdir()
        print_status("Created new 'bkp' secure vault directory")

    # 2. Create the ZIP Backup
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = BKP_DIR / f"mac-dev-os_offline_backup_{timestamp}.zip"
    
    # Ignore heavy/unnecessary folders AND the bkp folder itself
    ignore_dirs = {'.git', 'node_modules', '.next', '.vercel', '__pycache__', 'bkp'}
    
    print_status(f"Compressing current Matrix into: {zip_filename.name}")
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(PROJECT_PATH):
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                for file in files:
                    if not file.endswith('.zip'):
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, PROJECT_PATH)
                        zipf.write(file_path, arcname)
        print("  -> Backup successfully secured in /bkp folder.")
    except Exception as e:
        print(f"  -> [ERROR] Failed to zip: {e}")

def create_script_log():
    print_status("Compiling essential Python scripts into script.txt")
    script_txt_path = PROJECT_PATH / "script.txt"
    
    # We will try to read your master deployment script if it exists
    deploy_script_path = PROJECT_PATH / "step57_backup_and_push.py"
    deploy_content = "[File not found on disk]"
    if deploy_script_path.exists():
        with open(deploy_script_path, "r", encoding="utf-8") as f:
            deploy_content = f.read()

    # We also save THIS current script
    current_script_path = PROJECT_PATH / "step74_vault_manager.py"
    current_content = "[File not found on disk]"
    if current_script_path.exists():
        with open(current_script_path, "r", encoding="utf-8") as f:
            current_content = f.read()

    # Format the log
    log_content = f"""====================================================
      M.A.C.DevOS ESSENTIAL AUTOMATION SCRIPTS      
====================================================
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Below are the master scripts used to maintain, backup, 
and deploy the M.A.C.DevOS architecture.

----------------------------------------------------
SCRIPT 1: MASTER DEPLOY & BACKUP (step57_backup_and_push.py)
Description: Syncs with Git, creates a root backup, and pushes to Vercel.
----------------------------------------------------
{deploy_content}


----------------------------------------------------
SCRIPT 2: THE VAULT MANAGER (step74_vault_manager.py)
Description: Creates the /bkp folder, zips the project offline, and generates this script.txt file.
----------------------------------------------------
{current_content}

====================================================
[END OF SCRIPT LOG]
"""

    with open(script_txt_path, "w", encoding="utf-8") as f:
        f.write(log_content)
    print("  -> script.txt successfully generated in root directory.")

if __name__ == "__main__":
    create_vault_and_backup()
    create_script_log()
    print("\n[SUCCESS] System Vault fully updated and locked. Ready for next phase.")