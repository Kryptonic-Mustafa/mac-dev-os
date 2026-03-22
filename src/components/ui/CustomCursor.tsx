"use client";
import { useState, useEffect, useRef } from 'react';

export default function CustomCursor() {
  const [mounted, setMounted] = useState(false);
  const cursorDot = useRef<HTMLDivElement>(null);
  const cursorRing = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMounted(true);
    const moveCursor = (e: MouseEvent) => {
      if (cursorDot.current && cursorRing.current) {
        cursorDot.current.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        cursorRing.current.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
      }
    };
    window.addEventListener('mousemove', moveCursor);
    return () => window.removeEventListener('mousemove', moveCursor);
  }, []);

  if (!mounted) return null;

  return (
    <>
      <div ref={cursorDot} className="fixed top-0 left-0 w-1.5 h-1.5 bg-primary rounded-full pointer-events-none z-[999] -translate-x-1/2 -translate-y-1/2 transition-transform duration-75 ease-out" />
      <div ref={cursorRing} className="fixed top-0 left-0 w-8 h-8 border border-primary/30 rounded-full pointer-events-none z-[998] -translate-x-1/2 -translate-y-1/2 transition-transform duration-300 ease-out" />
    </>
  );
}
