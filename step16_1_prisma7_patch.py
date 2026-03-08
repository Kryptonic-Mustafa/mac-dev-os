import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🔧 M.A.C.DevOS Hotfix] {message}...")
    time.sleep(0.5)

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"❌ Error executing: {command}\n{stderr.decode('utf-8')}")
    return process.returncode == 0

def patch_prisma_v7():
    print_status("Patching Data Layer for Prisma V7 Architecture")

    # 1. Install the new V7 required driver adapters
    print_status("Installing MySQL2 and Prisma Adapter packages")
    run_command("npm install mysql2 @prisma/adapter-mysql", cwd=PROJECT_PATH)

    # 2. Strip the deprecated URL line from schema.prisma
    print_status("Updating schema.prisma to V7 standards")
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Filter out the URL line
        new_lines = [line for line in lines if 'url      = env("DATABASE_URL")' not in line]
        
        with open(schema_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

    # 3. Create the Database Singleton connection client
    print_status("Engineering Global V7 Database Singleton")
    lib_dir = PROJECT_PATH / "src/lib"
    os.makedirs(lib_dir, exist_ok=True)
    
    db_content = """import { PrismaClient } from '@prisma/client';
import { PrismaMysql } from '@prisma/adapter-mysql';
import mysql from 'mysql2/promise';

// Initialize the V7 Driver Adapter
const pool = mysql.createPool(process.env.DATABASE_URL as string);
const adapter = new PrismaMysql(pool);

// Cache the Prisma instance in development to prevent connection exhaustion
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({ adapter });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""
    with open(lib_dir / "db.ts", "w", encoding="utf-8") as f:
        f.write(db_content)

    print_status("Prisma V7 Patch Complete. System ready for deployment.")

if __name__ == "__main__":
    patch_prisma_v7()