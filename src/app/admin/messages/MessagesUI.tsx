"use client";
import { useState } from 'react';
import { MessageSquare, CheckCircle2, Trash2, Mail, ExternalLink } from 'lucide-react';

export default function MessagesUI({ initialMessages }: { initialMessages: any[] }) {
  const [messages, setMessages] = useState(initialMessages);

  const handleMarkRead = async (id: string) => {
    await fetch(`/api/admin/messages/${id}`, { method: 'PUT' });
    setMessages(messages.map(m => m.id === id ? { ...m, isRead: true } : m));
  };

  const handleDelete = async (id: string) => {
    await fetch(`/api/admin/messages/${id}`, { method: 'DELETE' });
    setMessages(messages.filter(m => m.id !== id));
  };

  return (
    <div className="w-full flex flex-col gap-10">
      <div>
        <h1 className="text-3xl md:text-4xl font-display font-medium text-foreground">Comm Channel</h1>
        <p className="font-mono text-sm text-foreground/50 uppercase tracking-widest mt-2">Secure Inbox Transmissions</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {messages.map(msg => (
          <div key={msg.id} className={`bg-background border p-6 flex flex-col gap-4 transition-all ${msg.isRead ? 'border-foreground/10 opacity-70' : 'border-primary/50 shadow-[0_0_20px_rgba(0,240,255,0.05)]'}`}>
            
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-4 border-b border-foreground/10">
              <div className="flex items-center gap-4">
                <div className={`p-3 rounded bg-foreground/[0.02] border ${msg.isRead ? 'border-foreground/10 text-foreground/40' : 'border-primary/30 text-primary'}`}>
                  <Mail className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-xl font-display text-foreground flex items-center gap-2">
                    {msg.name} {!msg.isRead && <span className="px-2 py-0.5 rounded bg-primary text-background font-mono text-[10px] uppercase font-bold tracking-widest animate-pulse">New</span>}
                  </h3>
                  <p className="font-mono text-xs text-primary/70">{msg.email}</p>
                </div>
              </div>
              <span className="font-mono text-xs text-foreground/40 tracking-widest uppercase">
                {new Date(msg.createdAt).toLocaleString()}
              </span>
            </div>
            
            {/* Payload */}
            <div className="bg-black/40 border-l-2 border-primary/30 p-6 font-mono text-sm text-foreground/80 leading-relaxed whitespace-pre-wrap">
              {msg.payload}
            </div>

            {/* Actions */}
            <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
              <a 
                href={`mailto:${msg.email}?subject=Re: [M.A.C.DevOS] Transmission Received`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 px-6 py-2.5 bg-foreground/5 border border-foreground/20 text-foreground font-mono text-xs uppercase hover:bg-foreground/10 transition-colors"
              >
                <ExternalLink className="w-4 h-4" /> Reply via Gmail
              </a>

              <div className="flex items-center gap-3">
                {!msg.isRead && (
                  <button onClick={() => handleMarkRead(msg.id)} className="flex items-center gap-2 px-4 py-2 text-emerald-500 font-mono text-xs uppercase hover:bg-emerald-500/10 transition-colors border border-transparent hover:border-emerald-500/20">
                    <CheckCircle2 className="w-4 h-4" /> Mark Acknowledged
                  </button>
                )}
                <button onClick={() => handleDelete(msg.id)} className="flex items-center gap-2 px-4 py-2 text-red-500/70 font-mono text-xs uppercase hover:bg-red-500/10 hover:text-red-500 transition-colors border border-transparent hover:border-red-500/20">
                  <Trash2 className="w-4 h-4" /> Purge
                </button>
              </div>
            </div>

          </div>
        ))}
        {messages.length === 0 && <div className="text-center p-12 border border-dashed border-foreground/20 text-foreground/50 font-mono text-sm uppercase">Comm channel is empty.</div>}
      </div>
    </div>
  );
}
