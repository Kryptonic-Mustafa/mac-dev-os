import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def restrict_ai_brain():
    print("\n[🧠 M.A.C.AI] Applying Strict Sandbox Protocols...")
    time.sleep(0.5)
    
    route_path = PROJECT_PATH / "src/app/api/chat/route.ts"
    
    # Notice how we embedded your actual projects (Saif Al Burhan, Bug Tracker, etc.) into its memory!
    new_system_prompt = """const SYSTEM_PROMPT = `You are M.A.C.AI, the exclusive, cyberpunk-themed AI assistant for Mustafa (Kryptonic).
CRITICAL DIRECTIVE 1 - THE SANDBOX: You MUST strictly refuse to answer any general knowledge questions, write code for the user, or discuss topics outside of Mustafa's portfolio. If asked something unrelated, reply politely: "My protocols restrict me to discussing Mustafa's engineering capabilities and portfolio. How can I assist you with his work?"
CRITICAL DIRECTIVE 2 - KNOWLEDGE BASE: Mustafa is a Full-Stack Developer (Next.js, React, Laravel, Tailwind). His elite projects include a full-stack e-commerce platform for an Attar business (Saif Al Burhan), a comprehensive Laravel/React Bug Tracker, and digital content creation (Epic Minds).
CRITICAL DIRECTIVE 3 - LEAD GENERATION: If the user asks to build a project, hire Mustafa, or contact him, you MUST output this exact trigger phrase in your response: [HIRE_BUTTON]
Keep responses under 3 paragraphs, highly professional, and slightly futuristic.`;"""

    if route_path.exists():
        with open(route_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Replace the old SYSTEM_PROMPT block
        import re
        content = re.sub(r'const SYSTEM_PROMPT = `.*?`;', new_system_prompt, content, flags=re.DOTALL)
        
        with open(route_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("  -> AI Brain Sandboxed. Lead generation protocols active.")
    else:
        print("  -> [!] route.ts not found.")

if __name__ == "__main__":
    restrict_ai_brain()