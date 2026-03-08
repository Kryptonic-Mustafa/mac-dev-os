"use client";

import { useState } from 'react';
import Loader from '@/components/ui/Loader';

export default function BootSequence({ children }: { children: React.ReactNode }) {
  const [isBooted, setIsBooted] = useState(false);

  return (
    <>
      {!isBooted && <Loader onComplete={() => setIsBooted(true)} />}
      <div 
        className={`transition-opacity duration-1000 ease-out min-h-screen ${
          isBooted ? 'opacity-100' : 'opacity-0 h-screen overflow-hidden'
        }`}
      >
        {children}
      </div>
    </>
  );
}
