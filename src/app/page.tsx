import Hero from "@/components/sections/Hero";
import Architecture from "@/components/sections/Architecture";
import Advantages from "@/components/sections/Advantages";
import TechStack from "@/components/sections/TechStack";
import DeploymentMatrix from "@/components/sections/Projects";
import SystemReviews from "@/components/sections/Reviews";
import Contact from "@/components/sections/Contact";

export default function Home() {
  return (
    <main className="flex flex-col w-full relative">
      <Hero />
      <Architecture />
      <Advantages />
      <TechStack />
      <DeploymentMatrix />
      <SystemReviews />
      <Contact />
    </main>
  );
}
