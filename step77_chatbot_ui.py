import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def print_status(message):
    print(f"\n[🤖 M.A.C.DevOS AI Module] {message}...")
    time.sleep(0.5)

def build_chatbot_ui():
    ui_dir = PROJECT_PATH / "src/components/ui"
    if not ui_dir.exists():
        ui_dir.mkdir(parents=True, exist_ok=True)
        
    chatbot_path = ui_dir / "Chatbot.tsx"
    
    react_code = """"use client";
import { useState, useRef, useEffect } from 'react';
import { Terminal, X, Send, Loader2, MessageSquareTerminal } from 'lucide-react';

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    { role: "bot", content: "M.A.C.DevOS Comm-Link initialized. How can I assist you with Mustafa's portfolio?" }
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setIsLoading(true);

    // TODO: We will replace this setTimeout with the actual Gemini API call in the next step!
    setTimeout(() => {
      setMessages(prev => [...prev, { role: "bot", content: "I am currently disconnected from the Gemini Neural Engine. Please stand by for API integration." }]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <>
      {/* FLOATING ACTION BUTTON */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 z-50 p-4 rounded-full bg-background border border-primary/50 text-primary shadow-[0_0_20px_rgba(0,255,128,0.2)] hover:shadow-[0_0_30px_rgba(0,255,128,0.5)] transition-all duration-300 ${isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}
      >
        <MessageSquareTerminal className="w-6 h-6" />
        {/* Notification Dot */}
        <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full animate-ping"></span>
        <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full shadow-[0_0_10px_rgba(0,255,128,1)]"></span>
      </button>

      {/* CHAT WINDOW */}
      <div 
        className={`fixed bottom-6 right-6 z-50 w-[90vw] sm:w-[400px] h-[600px] max-h-[80vh] flex flex-col bg-background/90 backdrop-blur-xl border border-primary/20 rounded-lg shadow-[0_0_40px_rgba(0,0,0,0.8)] transition-all duration-500 origin-bottom-right ${isOpen ? 'scale-100 opacity-100' : 'scale-90 opacity-0 pointer-events-none'}`}
      >
        {/* HEADER */}
        <div className="flex items-center justify-between p-4 border-b border-primary/20 bg-primary/5">
          <div className="flex items-center gap-2 text-primary font-mono text-sm">
            <Terminal className="w-5 h-5" />
            <span>M.A.C.DevOS AI</span>
          </div>
          <button onClick={() => setIsOpen(false)} className="text-foreground/50 hover:text-primary transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* MESSAGE LOG */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:bg-primary/20 [&::-webkit-scrollbar-track]:bg-transparent">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-[80%] p-3 rounded-md text-sm font-mono leading-relaxed ${
                  msg.role === 'user' 
                    ? 'bg-primary/20 border border-primary/30 text-primary rounded-br-none' 
                    : 'bg-foreground/5 border border-foreground/10 text-foreground/80 rounded-bl-none'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-foreground/5 border border-foreground/10 p-3 rounded-md rounded-bl-none flex items-center gap-2 text-primary">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-xs font-mono">Processing...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* INPUT FIELD */}
        <form onSubmit={handleSend} className="p-4 border-t border-primary/20 bg-background/50">
          <div className="relative flex items-center">
            <span className="absolute left-3 text-primary font-mono text-sm">{'>'}</span>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything..."
              className="w-full bg-foreground/5 border border-primary/30 focus:border-primary rounded-md py-3 pl-8 pr-12 text-sm font-mono text-foreground placeholder:text-foreground/30 focus:outline-none focus:ring-1 focus:ring-primary/50 transition-all"
            />
            <button 
              type="submit" 
              disabled={!input.trim() || isLoading}
              className="absolute right-2 p-2 text-foreground/50 hover:text-primary disabled:opacity-50 disabled:hover:text-foreground/50 transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
"""
    with open(chatbot_path, "w", encoding="utf-8") as f:
        f.write(react_code)
    
    print_status("Chatbot UI built successfully")

if __name__ == "__main__":
    build_chatbot_ui()