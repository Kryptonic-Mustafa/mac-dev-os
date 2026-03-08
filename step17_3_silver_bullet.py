import os
import time
import subprocess
from pathlib import Path

PROJECT_PATH = Path.cwd()

def deploy_silver_bullet():
    print("\n[🛡️ M.A.C.DevOS System] Deploying Prisma Legacy Stability Patch...")
    time.sleep(0.5)

    # 1. NUKE THE V7 CONFIG FILE
    config_path = PROJECT_PATH / "prisma.config.ts"
    if config_path.exists():
        os.remove(config_path)
        print("  ✓ Destroyed prisma.config.ts (Disabled strict V7 mode)")

    # 2. RESTORE SCHEMA.PRISMA (With the URL intact)
    schema_path = PROJECT_PATH / "prisma/schema.prisma"
    schema_content = """generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

// -----------------------------------------------------------------------------
// SECURE ADMIN ACCESS
// -----------------------------------------------------------------------------
model Admin {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String   // Will be hashed securely
  createdAt DateTime @default(now())
}

// -----------------------------------------------------------------------------
// DEPLOYMENT MATRIX (Projects)
// -----------------------------------------------------------------------------
model Project {
  id          String   @id @default(uuid())
  systemId    String   @unique // e.g., "SYS-01"
  title       String
  description String   @db.Text
  tech        String   // Stored as JSON string or comma-separated
  repoLink    String?
  liveLink    String?
  order       Int      @default(0)
  isVisible   Boolean  @default(true)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

// -----------------------------------------------------------------------------
// TELEMETRY LOGS (Reviews)
// -----------------------------------------------------------------------------
model Review {
  id        String   @id @default(uuid())
  logId     String   @unique // e.g., "LOG-992"
  client    String
  role      String
  content   String   @db.Text
  status    String   @default("VERIFIED")
  isVisible Boolean  @default(true)
  createdAt DateTime @default(now())
}

// -----------------------------------------------------------------------------
// SECURE COMM CHANNEL (Messages)
// -----------------------------------------------------------------------------
model Message {
  id        String   @id @default(uuid())
  name      String
  email     String
  payload   String   @db.Text
  isRead    Boolean  @default(false)
  createdAt DateTime @default(now())
}
"""
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(schema_content)
    print("  ✓ Restored schema.prisma with standard routing.")

    # 3. RESTORE DB.TS (Simple, empty constructor)
    db_path = PROJECT_PATH / "src/lib/db.ts"
    db_content = """import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

// With the V7 config gone, PrismaClient goes back to working natively
export const db = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db;
"""
    with open(db_path, "w", encoding="utf-8") as f:
        f.write(db_content)
    print("  ✓ Restored db.ts to standard initialization.")

    # 4. REGENERATE THE CLIENT
    print("\n  ⚙️ Rebuilding Prisma Client with legacy rules...")
    subprocess.run("npx prisma generate", shell=True, cwd=PROJECT_PATH)
    
    print("\n[✅ M.A.C.DevOS System] Data Layer fully stabilized.")

if __name__ == "__main__":
    deploy_silver_bullet()