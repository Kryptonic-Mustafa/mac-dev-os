import os
import time
from pathlib import Path

def generate_system_txt():
    print("\n[🖥️ M.A.C.DevOS Architect] Analyzing system vitals...")
    time.sleep(1)
    
    project_root = Path.cwd()
    output_file = project_root / "system.txt"
    
    # Define project metadata based on current state
    project_aim = "M.A.C.DevOS: A high-fidelity, OS-styled developer portfolio mimicking a terminal/macOS interface."
    tech_stack = "Next.js 16.1.6 (Turbopack), Prisma ORM, TiDB Cloud (MySQL), GSAP (Animations), Tailwind CSS, Lucide Icons."
    db_overview = "Relational database managed via TiDB Cloud. Tables: Admin (Auth), Project (Matrix Assets), Message (Comm Channel), SystemSettings."
    frontend_overview = "Component-based architecture using Next.js App Router. Features a custom GSAP-powered 'Neon Dev Station' boot sequence and a custom interactive cursor."

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("====================================================\n")
        f.write("           M.A.C.DevOS SYSTEM OVERVIEW              \n")
        f.write("====================================================\n\n")
        
        f.write(f"PROJECT AIM: {project_aim}\n")
        f.write(f"CORE ENGINE: {tech_stack}\n\n")
        
        f.write("--- SYSTEM ARCHITECTURE ---\n")
        f.write(f"FRONTEND: {frontend_overview}\n")
        f.write(f"DATABASE: {db_overview}\n")
        f.write("DEPLOYMENT: Vercel (CI/CD via GitHub)\n\n")
        
        f.write("--- DIRECTORY MAP ---\n")
        # Generate folder structure (skipping junk folders)
        skip_dirs = {'.next', 'node_modules', '.git', '.vercel'}
        
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            level = root.replace(str(project_root), '').count(os.sep)
            indent = ' ' * 4 * level
            f.write(f"{indent}[FOLDER] {os.path.basename(root)}/\n")
            sub_indent = ' ' * 4 * (level + 1)
            for file in files:
                if not file.startswith('.') and file != 'system.txt':
                    f.write(f"{sub_indent}{file}\n")
        
        f.write("\n--- KEY COMPONENT BREAKDOWN ---\n")
        f.write("- src/app/admin: The Restricted Command Center (Login/Dashboard/Settings).\n")
        f.write("- src/app/api: Serverless endpoints for DB interaction and Gmail transmission.\n")
        f.write("- src/components/ui: High-fidelity interactive elements (CustomCursor, Loader).\n")
        f.write("- prisma/schema.prisma: The master database blueprint.\n")
        
        f.write("\n--- DEPLOYMENT COMMANDS ---\n")
        f.write("Build: npx prisma generate && npx prisma db push && next build\n")
        f.write("Local Dev: npm run dev\n")
        
        f.write("\n[END OF SYSTEM LOG]")

    print(f"\n[✓] System Blueprint encoded to: {output_file}")

if __name__ == "__main__":
    generate_system_txt()