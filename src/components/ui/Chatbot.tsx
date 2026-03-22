"use client";
import { useState, useRef, useEffect } from 'react';
import { Terminal, X, Send, Loader2, Bot, Code2 } from 'lucide-react';

type Message = { role: 'user' | 'bot', content: string };

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const defaultMessage: Message = { role: "bot", content: "M.A.C.AI Online. I am restricted to discussing Mustafa's engineering portfolio. How may I assist your system today?" };
  const [messages, setMessages] = useState<Message[]>([defaultMessage]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedChat = localStorage.getItem('macdevos_chat_json');
    if (savedChat) {
      try { setMessages(JSON.parse(savedChat)); } catch (e) { }
    }
  }, []);

  useEffect(() => {
    if (messages.length > 1) {
      localStorage.setItem('macdevos_chat_json', JSON.stringify(messages));
    }
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setInput("");
    const newMessages: Message[] = [...messages, { role: "user", content: userMsg }];
    setMessages(newMessages);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      setMessages(prev => [...prev, { role: "bot", content: data.reply }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "bot", content: "SYSTEM ERROR: Connection to M.A.C.AI Neural Engine timed out." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearMemory = () => {
    localStorage.removeItem('macdevos_chat_json');
    setMessages([defaultMessage]);
  };

  // Parses the AI response to turn [HIRE_BUTTON] into a glowing link
  const renderMessageContent = (content: string) => {
    if (content.includes('[HIRE_BUTTON]')) {
      const parts = content.split('[HIRE_BUTTON]');
      return (
        <div className="whitespace-pre-wrap">
          {parts[0]}
          <a
            href="https://mail.google.com/mail/?view=cm&fs=1&to=macdevos53@gmail.com&su=Project%20Inquiry%20via%20M.A.C.DevOS"
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setIsOpen(false)} // This will close the chat window neatly when they click!
            className="inline-flex items-center gap-2 mt-3 px-4 py-2 bg-primary/20 hover:bg-primary/40 border border-primary text-primary rounded-md transition-all font-bold tracking-wider text-xs shadow-[0_0_15px_rgba(0,255,128,0.2)] w-full justify-center"
          >
            <Terminal className="w-4 h-4" />
            INITIATE COMM-LINK (GMAIL)
          </a>
          {parts[1]}
        </div>
      );
    }
    return <div className="whitespace-pre-wrap">{content}</div>;
  };

  return (
    <>
      <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${isOpen ? 'scale-0 opacity-0 pointer-events-none' : 'scale-100 opacity-100'}`}>
        {/* THE ANIMATED TOOLTIP */}
        <div className="absolute right-full mr-4 top-1/2 -translate-y-1/2 whitespace-nowrap bg-background/95 backdrop-blur-sm border border-primary/50 text-primary px-4 py-2 rounded-md font-mono text-xs shadow-[0_0_15px_rgba(0,255,128,0.2)] flex items-center gap-3">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
          HI, I AM M.A.C.AI
          <div className="absolute top-1/2 -right-1.5 -translate-y-1/2 w-3 h-3 bg-background border-r border-t border-primary/50 transform translate-x-[1px] rotate-45"></div>
        </div>

        {/* THE FLOATING BUTTON */}
        <button
          onClick={() => setIsOpen(true)}
          className="relative p-4 rounded-full bg-background border border-primary text-primary shadow-[0_0_20px_rgba(0,255,128,0.3)] hover:shadow-[0_0_30px_rgba(0,255,128,0.6)] transition-all duration-300 group"
        >
          <div className="relative flex items-center justify-center">
            <Bot className="w-6 h-6 group-hover:scale-110 transition-transform" />
            <Code2 className="w-3 h-3 absolute -bottom-1 -right-1 bg-background rounded-full" />
          </div>
          <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full animate-ping"></span>
          <span className="absolute top-0 right-0 w-3 h-3 bg-primary rounded-full shadow-[0_0_10px_rgba(0,255,128,1)]"></span>
        </button>
      </div>

      {/* CHAT WINDOW */}
      <div className={`fixed bottom-6 right-6 z-50 w-[90vw] sm:w-[400px] h-[600px] max-h-[80vh] flex flex-col bg-background/90 backdrop-blur-xl border border-primary/40 rounded-lg shadow-[0_0_40px_rgba(0,0,0,0.8)] transition-all duration-500 origin-bottom-right ${isOpen ? 'scale-100 opacity-100' : 'scale-90 opacity-0 pointer-events-none'}`}>
        <div className="flex items-center justify-between p-4 border-b border-primary/30 bg-primary/10">
          <div className="flex items-center gap-2 text-primary font-mono text-sm font-bold tracking-widest">
            <Bot className="w-5 h-5" />
            <span>M.A.C.AI</span>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={clearMemory} className="text-[10px] font-mono text-foreground/40 hover:text-red-400 transition-colors uppercase">[ Wipe ]</button>
            <button onClick={() => setIsOpen(false)} className="text-foreground/50 hover:text-primary transition-colors"><X className="w-5 h-5" /></button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-4 [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-thumb]:bg-primary/20 [&::-webkit-scrollbar-track]:bg-transparent">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[85%] p-3 rounded-md text-sm font-mono leading-relaxed ${msg.role === 'user' ? 'bg-primary/20 border border-primary/40 text-primary rounded-br-none' : 'bg-foreground/5 border border-foreground/10 text-foreground/90 rounded-bl-none'}`}>
                {renderMessageContent(msg.content)}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-foreground/5 border border-foreground/10 p-3 rounded-md rounded-bl-none flex items-center gap-2 text-primary">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-xs font-mono">Consulting Archives...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSend} className="p-4 border-t border-primary/30 bg-background/80">
          <div className="relative flex items-center">
            <span className="absolute left-3 text-primary font-mono text-sm">{'>'}</span>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Query M.A.C.AI..." className="w-full bg-foreground/5 border border-primary/40 focus:border-primary rounded-md py-3 pl-8 pr-12 text-sm font-mono text-foreground placeholder:text-foreground/40 focus:outline-none focus:ring-1 focus:ring-primary/50 transition-all" />
            <button type="submit" disabled={!input.trim() || isLoading} className="absolute right-2 p-2 text-foreground/50 hover:text-primary disabled:opacity-50 disabled:hover:text-foreground/50 transition-colors"><Send className="w-4 h-4" /></button>
          </div>
        </form>
      </div>
    </>
  );
}
