import type { Metadata } from "next";
import { Inter, Space_Grotesk, JetBrains_Mono } from "next/font/google";
import BootSequence from "@/components/layout/BootSequence";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";
import BackgroundFX from "@/components/ui/BackgroundFX";
import CustomCursor from "@/components/ui/CustomCursor";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space-grotesk" });
const jetbrainsMono = JetBrains_Mono({ subsets: ["latin"], variable: "--font-jetbrains-mono" });

export const metadata: Metadata = {
  title: "M.A.C.DevOS | Premium Digital Engineering",
  description: "Advanced full-stack engineering and UI systems architecture.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${spaceGrotesk.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans antialiased bg-background text-foreground selection:bg-primary selection:text-background relative">
        <BackgroundFX />
        <CustomCursor />
        <BootSequence>
          <Navbar />
          <div className="flex-grow">
            {children}
          </div>
          <Footer />
        </BootSequence>
      </body>
    </html>
  );
}
