import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🗄️ M.A.C.DevOS Data Layer] {message}...")
    time.sleep(0.5)

def deploy_database_schema():
    if not (PROJECT_PATH / "prisma").exists():
        print("❌ Error: 'prisma' directory not found. Did Prisma initialize correctly in Step 1?")
        return

    print_status("Writing Prisma Relational Schema")
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

    print_status("Prisma Schema configured successfully.")
    
if __name__ == "__main__":
    deploy_database_schema()