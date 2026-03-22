import os
import time
from pathlib import Path

PROJECT_PATH = Path.cwd()

def wire_chatbot_ui():
    print("\n[🔌 M.A.C.DevOS UI Sync] Wiring frontend to the Neural API...")
    time.sleep(0.5)
    
    chatbot_path = PROJECT_PATH / "src/components/ui/Chatbot.tsx"
    
    react_code = """"use client";
import { useState, useRef, useEffect } from 'react';
import { Terminal, X, Send, Loader2, MessageSquare } from 'lucide-react';

type Message = { role: 'user' | 'bot', content: string };

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  
  // Default greeting
  const defaultMessage: Message = { role: "bot", content: "M.A.C.DevOS Comm-Link initialized. How can I assist you with Mustafa's portfolio architecture?" };
  
  const [messages, setMessages] = useState<Message[]>([defaultMessage]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // LOAD MEMORY: Check if the user has a saved JSON chat history in their browser
  useEffect(() => {
    const savedChat = localStorage.getItem('macdevos_chat_json');
    if (savedChat) {
      try {
        setMessages(JSON.parse(savedChat));
      } catch (e) {
        console.error("Corrupted chat memory reset.");
      }
    }
  }, []);

  // SAVE MEMORY: Every time messages update, save the JSON to the browser
  useEffect(() => {
    if (messages.length > 1) { // Don't save if it's just the default greeting
        localStorage.setItem('macdevos_chat_json', JSON.stringify(messages));
    }
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput("");
    
    // Optimistically add user message to the JSON array
    const newMessages: Message[] = [...messages, { role: "user", content: userMsg }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      // Send the entire JSON history to our Next.js backend
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.error);

      // Add the AI's response to the JSON array
      setMessages(prev => [...prev, { role: "bot", content: data.reply }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "bot", content: "SYSTEM ERROR: Connection to Neural Engine timed out. Please check logs." }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to clear chat memory
  const clearMemory = () => {
    localStorage.removeItem('macdevos_chat_json');
    setMessages([defaultMessage]);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed bottom-6 right-6 z-50 p-4 rounded-full bg-background border border-primary/50 text-primary shadow-[0_0_20px_rgba(0,255,128,0.2)] hover:shadow-[0_0_30px_rgba(0,255,128,0.5)] transition-all duration-300 ${isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}
      >
        <MessageSquare className="w-6 h-6" />
        <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full animate-ping"></span>
        <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full shadow-[0_0_10px_rgba(0,255,128,1)]"></span>
      </button>

      <div 
        className={`fixed bottom-6 right-6 z-50 w-[90vw] sm:w-[400px] h-[600px] max-h-[80vh] flex flex-col bg-background/90 backdrop-blur-xl border border-primary/20 rounded-lg shadow-[0_0_40px_rgba(0,0,0,0.8)] transition-all duration-500 origin-bottom-right ${isOpen ? 'scale-100 opacity-100' : 'scale-90 opacity-0 pointer-events-none'}`}
      >
        <div className="flex items-center justify-between p-4 border-b border-primary/20 bg-primary/5">
          <div className="flex items-center gap-2 text-primary font-mono text-sm">
            <Terminal className="w-5 h-5" />
            <span>M.A.C.DevOS AI</span>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={clearMemory} className="text-[10px] font-mono text-foreground/30 hover:text-red-400 transition-colors uppercase">
              [ Wipe Memory ]
            </button>
            <button onClick={() => setIsOpen(false)} className="text-foreground/50 hover:text-primary transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:bg-primary/20 [&::-webkit-scrollbar-track]:bg-transparent">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-[80%] p-3 rounded-md text-sm font-mono leading-relaxed whitespace-pre-wrap ${
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
                <span className="text-xs font-mono">Processing payload...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

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
    if chatbot_path.exists():
        with open(chatbot_path, "w", encoding="utf-8") as f:
            f.write(react_code)
        print("  -> UI successfully wired to /api/chat.")
    else:
        print("  -> [!] Chatbot.tsx not found.")

if __name__ == "__main__":
    wire_chatbot_ui()