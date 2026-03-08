import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🌀 M.A.C.DevOS Matrix Reset] {message}...")
    time.sleep(0.5)

def force_review_sync():
    # 1. VERIFY SCHEMA
    print_status("Checking Prisma Schema for Review Model")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Ensure Review model is actually in the file
    if "model Review" not in content:
        print_status("Review model missing from schema. Injecting now...")
        review_model = """
model Review {
  id        String   @id @default(uuid())
  logId     String   @unique 
  client    String
  role      String
  content   String   @db.Text
  status    String   @default("VERIFIED")
  isVisible Boolean  @default(true)
  createdAt DateTime @default(now())
}
"""
        with open(schema_path, "a", encoding="utf-8") as f:
            f.write(review_model)

    # 2. PHYSICAL DATABASE SYNC
    print_status("Physically Creating Review Table in MySQL")
    # This command creates the missing table in your macdevos database
    subprocess.run("npx prisma db push", shell=True, cwd=PROJECT_PATH)

    # 3. CLIENT REGENERATION
    print_status("Regenerating Prisma Client to acknowledge Review model")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)

    print_status("Sync Complete. Table should now appear in MySQL Workbench.")

if __name__ == "__main__":
    force_review_sync()