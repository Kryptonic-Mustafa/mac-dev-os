import os
import time

def print_status(message):
    print(f"\n[🔐 M.A.C.DevOS Security] {message}...")
    time.sleep(0.5)

def generate_seed_script():
    print_status("Aligning Payload with Prisma Schema (Email/Password Only)")
    
    js_content = """
const { PrismaClient } = require('@prisma/client');
let bcrypt;
try { bcrypt = require('bcryptjs'); } 
catch(e) { bcrypt = require('bcrypt'); }

const prisma = new PrismaClient();

async function seedAdmin() {
    try {
        console.log("\\n[!] Connecting to Live TiDB Database...");
        
        // This securely hashes the password
        const hash = await bcrypt.hash("macdevos2026", 10);
        
        const existing = await prisma.admin.findFirst();
        if (existing) {
            console.log("[✓] Admin already exists. You are good to go!");
            process.exit(0);
        }

        // FLAWLESS INJECTION: Only passing what your schema actually accepts
        await prisma.admin.create({
            data: {
                email: "admin@macdevos.com", 
                password: hash
            }
        });
        
        console.log("\\n=========================================");
        console.log("✅ LIVE MASTER ADMIN SUCCESSFULLY FORGED!");
        console.log("=========================================");
        console.log("👤 Email:     admin@macdevos.com");
        console.log("🔑 Password:  macdevos2026");
        console.log("=========================================\\n");

    } catch (error) {
        console.error("\\n❌ ERROR: Could not insert Admin.\\n", error);
    } finally {
        await prisma.$disconnect();
    }
}

seedAdmin();
"""
    with open("seed_live_admin.js", "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print_status("Executing Final Seed Script directly to TiDB...")
    os.system("node seed_live_admin.js")

if __name__ == "__main__":
    generate_seed_script()