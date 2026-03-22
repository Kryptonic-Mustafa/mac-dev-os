import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🧠 M.A.C.DevOS Neural Engine] {message}...")
    time.sleep(0.5)

def build_api_route():
    api_dir = PROJECT_PATH / "src/app/api/chat"
    if not api_dir.exists():
        api_dir.mkdir(parents=True, exist_ok=True)
        
    route_path = api_dir / "route.ts"
    
    # We are injecting a base System Prompt here. You can expand this later!
    api_code = """import { GoogleGenerativeAI } from '@google/generative-ai';
import { NextResponse } from 'next/server';

// Initialize the Gemini API safely using the hidden .env variable
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

// THE SYSTEM PROMPT: This tells the AI who it is and how to act.
const SYSTEM_PROMPT = `You are the M.A.C.DevOS Comm-Link, a highly advanced, cyberpunk-themed AI assistant built into the portfolio operating system of a Full-Stack Developer named Mustafa (also known as Kryptonic).
Your job is to assist recruiters and visitors. Keep your answers concise, highly professional, slightly futuristic, and deeply knowledgeable about web development (Next.js, React, Tailwind, GSAP, Laravel, Docker).
If someone asks about Mustafa's skills, emphasize his ability to build complex, optimized, full-stack architectures and his elite problem-solving skills.
Do NOT use markdown headers, just plain conversational text. Keep responses under 3 paragraphs.`;

export async function POST(req: Request) {
  try {
    // Receive the full JSON chat history from the frontend
    const { messages } = await req.json();

    // Initialize the specific Gemini model
    const model = genAI.getGenerativeModel({ 
        model: "gemini-1.5-flash",
        systemInstruction: SYSTEM_PROMPT
    });

    // Gemini requires a specific JSON structure: { role: 'user' | 'model', parts: [{ text: '...' }] }
    // We map your frontend JSON history into Gemini's format, excluding the very last message.
    const formattedHistory = messages.slice(0, -1).map((msg: any) => ({
      role: msg.role === 'bot' ? 'model' : 'user',
      parts: [{ text: msg.content }]
    }));

    // Extract the latest message the user just typed
    const latestMessage = messages[messages.length - 1].content;

    // Start the chat with the historical JSON context
    const chat = model.startChat({ history: formattedHistory });
    
    // Send the new message and wait for the AI to think
    const result = await chat.sendMessage(latestMessage);
    const response = await result.response;
    const text = response.text();

    // Return the AI's response as a JSON object
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
    with open(route_path, "w", encoding="utf-8") as f:
        f.write(api_code)
    
    print_status("Secure API Route (/api/chat) successfully established")

if __name__ == "__main__":
    build_api_route()