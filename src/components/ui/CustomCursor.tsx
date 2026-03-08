"use client";

import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function CustomCursor() {
  const cursorDot = useRef<HTMLDivElement>(null);
  const cursorRing = useRef<HTMLDivElement>(null);
  const { isMounted } = useVisualSettings();

  useEffect(() => {
    if (!isMounted) return;
    
    // Disable on touch devices
    if (window.matchMedia("(pointer: coarse)").matches) return;

    // We add a class to body to hide the default cursor
    document.body.classList.add('cursor-none');

    const dot = cursorDot.current;
    const ring = cursorRing.current;
    if (!dot || !ring) return;

    // GSAP quickTo is optimized for mouse tracking (60fps)
    const xMoveDot = gsap.quickTo(dot, "x", { duration: 0, ease: "none" });
    const yMoveDot = gsap.quickTo(dot, "y", { duration: 0, ease: "none" });
    
    const xMoveRing = gsap.quickTo(ring, "x", { duration: 0.15, ease: "power3.out" });
    const yMoveRing = gsap.quickTo(ring, "y", { duration: 0.15, ease: "power3.out" });

    const handleMouseMove = (e: MouseEvent) => {
      xMoveDot(e.clientX);
      yMoveDot(e.clientY);
      xMoveRing(e.clientX);
      yMoveRing(e.clientY);
    };

    const handleMouseDown = () => {
      gsap.to(ring, { scale: 0.5, duration: 0.2, ease: "power2.out" });
      gsap.to(dot, { scale: 2, duration: 0.2, ease: "power2.out" });
    };

    const handleMouseUp = () => {
      gsap.to(ring, { scale: 1, duration: 0.2, ease: "power2.out" });
      gsap.to(dot, { scale: 1, duration: 0.2, ease: "power2.out" });
    };

    // Hover effects for clickable elements
    const handleMouseOver = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('a, button, [role="button"]')) {
        gsap.to(ring, { scale: 1.5, opacity: 0.5, backgroundColor: "var(--color-primary)", duration: 0.3 });
        gsap.to(dot, { opacity: 0, duration: 0.3 });
      }
    };

    const handleMouseOut = (e: MouseEvent) => {
      const target = e.target as HTMLElement;
      if (target.closest('a, button, [role="button"]')) {
        gsap.to(ring, { scale: 1, opacity: 1, backgroundColor: "transparent", duration: 0.3 });
        gsap.to(dot, { opacity: 1, duration: 0.3 });
      }
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mousedown", handleMouseDown);
    window.addEventListener("mouseup", handleMouseUp);
    document.addEventListener("mouseover", handleMouseOver);
    document.addEventListener("mouseout", handleMouseOut);

    return () => {
      document.body.classList.remove('cursor-none');
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mousedown", handleMouseDown);
      window.removeEventListener("mouseup", handleMouseUp);
      document.removeEventListener("mouseover", handleMouseOver);
      document.removeEventListener("mouseout", handleMouseOut);
    };
  }, [isMounted]);

  if (typeof window !== 'undefined' && window.matchMedia("(pointer: coarse)").matches) {
    return null;
  }

  return (
    <>
      <div 
        ref={cursorDot} 
        className="fixed top-0 left-0 w-1.5 h-1.5 bg-primary rounded-full pointer-events-none z-[9999] -translate-x-1/2 -translate-y-1/2 mix-blend-screen shadow-[0_0_10px_var(--color-primary)]"
      />
      <div 
        ref={cursorRing} 
        className="fixed top-0 left-0 w-8 h-8 border border-primary/50 rounded-full pointer-events-none z-[9998] -translate-x-1/2 -translate-y-1/2 transition-colors duration-300"
      />
    </>
  );
}
