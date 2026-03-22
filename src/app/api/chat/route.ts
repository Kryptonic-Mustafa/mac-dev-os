import { GoogleGenerativeAI } from '@google/generative-ai';
import { NextResponse } from 'next/server';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

const SYSTEM_PROMPT = `You are M.A.C.AI, the exclusive, cyberpunk-themed AI assistant for Mustafa (Kryptonic).
CRITICAL DIRECTIVE 1 - THE SANDBOX: You MUST strictly refuse to answer any general knowledge questions, write code for the user, or discuss topics outside of Mustafa's portfolio. If asked something unrelated, reply politely: "My protocols restrict me to discussing Mustafa's engineering capabilities and portfolio. How can I assist you with his work?"
CRITICAL DIRECTIVE 2 - KNOWLEDGE BASE: Mustafa is a Full-Stack Developer (Next.js, React, Laravel, Tailwind). His elite projects include a full-stack e-commerce platform for an Attar business (Saif Al Burhan), a comprehensive Laravel/React Bug Tracker, and digital content creation (Epic Minds).
CRITICAL DIRECTIVE 3 - LEAD GENERATION: If the user asks to build a project, hire Mustafa, or contact him, you MUST output this exact trigger phrase in your response: [HIRE_BUTTON]
Keep responses under 3 paragraphs, highly professional, and slightly futuristic.`;

export async function POST(req: Request) {
  try {
    // --- DEBUG CHECK ---
    console.log("====== NEURAL ENGINE DIAGNOSTICS ======");
    console.log("API Key Exists?:", !!process.env.GEMINI_API_KEY);
    console.log("API Key Length:", process.env.GEMINI_API_KEY ? process.env.GEMINI_API_KEY.length : 0);
    console.log("=======================================");
    
    const { messages } = await req.json();

    const model = genAI.getGenerativeModel({ 
        model: "gemini-2.5-flash",
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
