import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def fix_api_route():
    print("\n[🧠 M.A.C.DevOS Neural Engine] Patching Gemini History rules...")
    time.sleep(0.5)
    
    route_path = PROJECT_PATH / "src/app/api/chat/route.ts"
    
    api_code = """import { GoogleGenerativeAI } from '@google/generative-ai';
import { NextResponse } from 'next/server';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

const SYSTEM_PROMPT = `You are the M.A.C.DevOS Comm-Link, a highly advanced, cyberpunk-themed AI assistant built into the portfolio operating system of a Full-Stack Developer named Mustafa (also known as Kryptonic).
Your job is to assist recruiters and visitors. Keep your answers concise, highly professional, slightly futuristic, and deeply knowledgeable about web development (Next.js, React, Tailwind, GSAP, Laravel, Docker).
If someone asks about Mustafa's skills, emphasize his ability to build complex, optimized, full-stack architectures and his elite problem-solving skills.
Do NOT use markdown headers, just plain conversational text. Keep responses under 3 paragraphs.`;

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    const model = genAI.getGenerativeModel({ 
        model: "gemini-1.5-flash",
        systemInstruction: SYSTEM_PROMPT
    });

    // Map the frontend JSON to Gemini's format
    let formattedHistory = messages.slice(0, -1).map((msg: any) => ({
      role: msg.role === 'bot' ? 'model' : 'user',
      parts: [{ text: msg.content }]
    }));

    // CRITICAL FIX: Gemini requires the history to ALWAYS start with a 'user' message.
    // If the first message in our history is the bot's default greeting, remove it.
    if (formattedHistory.length > 0 && formattedHistory[0].role === 'model') {
        formattedHistory.shift(); 
    }

    const latestMessage = messages[messages.length - 1].content;

    const chat = model.startChat({ history: formattedHistory });
    const result = await chat.sendMessage(latestMessage);
    const response = await result.response;
    const text = response.text();

    return NextResponse.json({ reply: text });

  } catch (error) {
    console.error("Neural Engine Error:", error);
    return NextResponse.json(
      { error: "Comm-Link failure. The Neural Engine is currently offline." }, 
      { status: 500 }
    );
  }
}
"""
    if route_path.exists():
        with open(route_path, "w", encoding="utf-8") as f:
            f.write(api_code)
        print("  -> History logic patched. Gemini will now accept the payload.")
    else:
        print("  -> [!] route.ts not found.")

if __name__ == "__main__":
    fix_api_route()