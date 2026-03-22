"use client";

import { useEffect, useRef } from 'react';
import { useVisualSettings } from '@/lib/storage/visualStorage';

export default function BackgroundFX() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { isMounted } = useVisualSettings();

  useEffect(() => {
    if (!isMounted || !canvasRef.current) return;
    
    // Only run heavy FX on non-touch devices
    const isTouch = window.matchMedia("(pointer: coarse)").matches;
    if (isTouch) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let particles: Particle[] = [];
    const mouse = { x: -1000, y: -1000, active: false };

    // Get primary color from computed CSS variables
    const getPrimaryColor = () => {
      const root = document.documentElement;
      const color = getComputedStyle(root).getPropertyValue('--color-primary').trim();
      return color || '#00F0FF';
    };

    class Particle {
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;

      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 1.5;
      }

      update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      }

      draw() {
        if (!ctx) return;
        ctx.fillStyle = getPrimaryColor();
        ctx.globalAlpha = 0.2;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    const init = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      particles = [];
      const particleCount = Math.floor((canvas.width * canvas.height) / 15000); // Responsive amount
      for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const color = getPrimaryColor();

      // Keyboard activity visual burst effect
      ctx.fillStyle = color;

      particles.forEach((p, index) => {
        p.update();
        p.draw();

        // Connect particles near mouse (Hacker Nexus Effect)
        if (mouse.active) {
          const dx = mouse.x - p.x;
          const dy = mouse.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 150) {
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.globalAlpha = 1 - dist / 150;
            ctx.lineWidth = 0.5;
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(mouse.x, mouse.y);
            ctx.stroke();
          }
        }
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    // Event Listeners
    const handleMouseMove = (e: MouseEvent) => {
      mouse.x = e.clientX;
      mouse.y = e.clientY;
      mouse.active = true;
    };
    
    const handleMouseLeave = () => { mouse.active = false; };
    const handleResize = () => { init(); };

    // Keyboard trigger (draws a scanning line)
    const handleKeyDown = () => {
       ctx.fillStyle = getPrimaryColor();
       ctx.globalAlpha = 0.05;
       ctx.fillRect(0, Math.random() * canvas.height, canvas.width, 2);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('touchmove', (e) => handleMouseMove(e.touches[0] as any), { passive: true });
    window.addEventListener('touchstart', (e) => handleMouseMove(e.touches[0] as any), { passive: true });
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('resize', handleResize);
    window.addEventListener('keydown', handleKeyDown);

    init();
    animate();

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('touchmove', handleMouseMove);
      window.removeEventListener('touchstart', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [isMounted]);

  return (
    <canvas 
      ref={canvasRef} 
      className="fixed inset-0 pointer-events-none z-0 opacity-40 transition-opacity duration-1000"
    />
  );
}
