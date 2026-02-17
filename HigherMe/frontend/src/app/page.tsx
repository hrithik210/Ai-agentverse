'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ArrowRight, Zap, Target, Code, Leaf, Shield, Flame, Sword, Scroll } from 'lucide-react';
import gsap from 'gsap';
import * as THREE from 'three';

export default function LandingPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const heroRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // GSAP Animations
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: "power3.out" } });
      
      tl.from(".hero-text", {
        y: 50,
        opacity: 0,
        duration: 1.2,
        stagger: 0.15
      })
      .from(".hero-btn", {
        scale: 0.8,
        opacity: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: "back.out(1.7)"
      }, "-=0.5")
      .from(".feature-card", {
        y: 100,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1
      }, "-=0.3");
    }, heroRef);

    // Three.js Background (Bioluminescent Swarm)
    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050A06, 0.05); // Dark forest fog
    
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ 
      canvas: canvasRef.current, 
      alpha: true,
      antialias: true 
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create Fireflies/Spores
    const geometry = new THREE.BufferGeometry();
    const count = 200;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 30; // x
      positions[i * 3 + 1] = (Math.random() - 0.5) * 30; // y
      positions[i * 3 + 2] = (Math.random() - 0.5) * 30; // z
      
      // Random green hues
      colors[i * 3] = 0.2 + Math.random() * 0.2; // R
      colors[i * 3 + 1] = 0.8 + Math.random() * 0.2; // G (High green)
      colors[i * 3 + 2] = 0.2 + Math.random() * 0.4; // B
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.15,
      vertexColors: true,
      transparent: true,
      opacity: 0.8,
      blending: THREE.AdditiveBlending
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    camera.position.z = 10;

    // Mouse Intreraction
    let mouseX = 0;
    let mouseY = 0;
    
    const handleMouseMove = (e: MouseEvent) => {
      mouseX = (e.clientX / window.innerWidth) * 2 - 1;
      mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    };

    window.addEventListener('mousemove', handleMouseMove);

    // Animation Loop
    const animate = () => {
      requestAnimationFrame(animate);

      // Gentle swarm movement
      const time = Date.now() * 0.0005;
      particles.rotation.x = time * 0.1;
      particles.rotation.y = time * 0.05;
      
      // Mouse sway
      particles.rotation.x += mouseY * 0.05;
      particles.rotation.y += mouseX * 0.05;
      
      // Pulse size
      material.size = 0.15 + Math.sin(time * 2) * 0.05;

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      ctx.revert();
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="min-h-screen bg-transparent text-foreground flex flex-col relative overflow-hidden font-sans selection:bg-primary/30 selection:text-primary-foreground">
      {/* 3D Background Canvas */}
      <canvas 
        ref={canvasRef} 
        className="fixed top-0 left-0 w-full h-full pointer-events-none z-0"
      />



      {/* Header - Premium Grounded Look (Kept from V3 based on feedback) */}
      <header className="fixed top-0 w-full z-50 bg-[#050A06]/80 backdrop-blur-xl border-b border-white/5 supports-[backdrop-filter]:bg-[#050A06]/60">
        <div className="container mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-3 group cursor-pointer">
            <div className="relative flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-primary/20 to-primary/5 border border-primary/20 group-hover:border-primary/50 transition-colors duration-500 overflow-hidden">
              <div className="absolute inset-0 bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <Leaf className="w-5 h-5 text-primary relative z-10" />
            </div>
            <span className="font-bold text-xl tracking-tight text-white/90">HigherMe</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
            <Link href="#quests" className="hover:text-primary transition-colors">Quests</Link>
            <Link href="#inventory" className="hover:text-primary transition-colors">Inventory</Link>
            <Link href="#guild" className="hover:text-primary transition-colors">Guild</Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link href="/signin">
              <Button variant="ghost" className="text-sm font-medium text-muted-foreground hover:text-white hover:bg-white/5">
                Log In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="lush" className="text-sm font-semibold h-10 px-6 shadow-none hover:shadow-[0_0_20px_-5px_var(--primary)] text-black">
                Start Game
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 pt-24 relative z-10" ref={heroRef}>
        {/* Hero Section (Reverted to Gamified V2) */}
        <section className="container mx-auto px-4 py-24 lg:py-32 text-center">
          <div className="max-w-5xl mx-auto space-y-8">
            <div className="hero-text inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-mono font-bold border border-primary/30 uppercase tracking-widest">
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-primary animate-ping"></span>
                System Online: v2.0
              </span>
            </div>
            
            <h1 className="hero-text text-5xl lg:text-8xl font-black tracking-tight text-white leading-[1] drop-shadow-[0_0_25px_rgba(74,222,128,0.3)]">
              Log Your Life. <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-[#86EFAC] to-primary animate-gradient-x">
                Level Up Your Stats.
              </span>
            </h1>
            
            <p className="hero-text text-lg lg:text-2xl text-muted-foreground max-w-2xl mx-auto leading-relaxed font-medium">
              This isn't just a productivity app. It's an RPG where <span className="text-white font-bold">YOU</span> are the main character. Track your grind, farm XP, and maximize your skill tree.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8">
              <Link href="/signup" className="hero-btn">
                <Button variant="lush" size="lg" className="rounded-xl px-12 h-16 text-xl font-black tracking-wide shadow-[0_0_30px_rgba(74,222,128,0.4)] hover:shadow-[0_0_50px_rgba(74,222,128,0.6)] hover:scale-105 transition-all duration-300 border-2 border-primary/50">
                  <Flame className="mr-2 w-6 h-6 fill-current" />
                  NEW GAME
                </Button>
              </Link>
              <Link href="#quests" className="hero-btn">
                <Button variant="outline" size="lg" className="rounded-xl px-10 h-16 text-lg border-white/10 bg-white/5 hover:bg-white/10 hover:text-white backdrop-blur-md text-gray-300">
                  <Scroll className="mr-2 w-5 h-5" />
                  View Quest Log
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Stats Grid (Reverted to Gamified V2 but polished) */}
        <section id="quests" className="container mx-auto px-4 py-20">
          <div className="grid md:grid-cols-3 gap-6 max-w-7xl mx-auto">
            {[
              {
                icon: <Target className="w-12 h-12 text-primary" />,
                title: "Mood Inventory",
                stat: "+INT",
                description: "Log your daily mental state to buff your Intelligence stats. Identify debuffs before they drain your mana."
              },
              {
                icon: <Shield className="w-12 h-12 text-primary" />,
                title: "Health HP",
                stat: "+VIT",
                description: "Track nutrition and sleep to keep your HP bar full. Don't let your stamina deplete during a grind session."
              },
              {
                icon: <Code className="w-12 h-12 text-primary" />,
                title: "Skill Tree",
                stat: "+DEX",
                description: "Visualize your coding progress. Commit code daily to maintain your combo streak and unlock new achievements."
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="feature-card lush-glass p-8 rounded-3xl lush-card-hover group relative overflow-hidden border border-white/5 hover:border-primary/50 transition-colors duration-500"
              >
                <div className="absolute top-4 right-4 text-xs font-mono text-primary/60 border border-primary/20 px-2 py-1 rounded">
                  {feature.stat}
                </div>
                <div className="mb-6 p-4 bg-primary/10 rounded-2xl w-fit text-primary ring-1 ring-primary/30 group-hover:bg-primary group-hover:text-black transition-colors duration-300">
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-white font-mono">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Level Up Section (Redesigned Social Proof) */}
        <section className="container mx-auto px-4 py-24 pb-40">
          <div className="max-w-5xl mx-auto border border-white/10 bg-[#0C1F12]/60 backdrop-blur-md rounded-[2rem] overflow-hidden relative">
             <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_-20%,rgba(74,222,128,0.1),transparent_70%)]" />
             
             <div className="grid md:grid-cols-2 gap-0 relative z-10">
                <div className="p-12 flex flex-col justify-center space-y-8 border-b md:border-b-0 md:border-r border-white/5">
                   <div>
                      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-primary/10 text-primary text-xs font-mono mb-4 border border-primary/20">
                        <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                        SERVER STATUS: ONLINE
                      </div>
                      <h2 className="text-4xl md:text-5xl font-black text-white font-mono tracking-tighter mb-4">
                        JOIN THE <br/> <span className="text-primary">GUILD</span>
                      </h2>
                      <p className="text-muted-foreground text-lg px-1">
                        Compete with yourself. Unlock achievements. Master your daily routine.
                      </p>
                   </div>
                   
                   <div className="flex gap-4">
                      <Link href="/signup">
                        <Button className="h-14 px-8 text-lg font-bold bg-primary text-black hover:bg-white hover:text-black transition-all">
                          Create Account
                        </Button>
                      </Link>
                      <Link href="/login">
                        <Button variant="ghost" className="h-14 px-8 text-lg text-white hover:bg-white/5">
                           Login
                        </Button>
                      </Link>
                   </div>
                </div>

                <div className="p-12 bg-black/20 flex flex-col justify-center">
                   <div className="space-y-6">
                      <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                         <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                               <Sword className="w-5 h-5" />
                            </div>
                            <div>
                               <div className="text-sm text-muted-foreground font-mono uppercase">Active Players</div>
                               <div className="text-2xl font-bold text-white">12,405</div>
                            </div>
                         </div>
                      </div>

                      <div className="flex items-center justify-between p-4 rounded-xl bg-white/5 border border-white/5">
                         <div className="flex items-center gap-4">
                            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-primary">
                               <Scroll className="w-5 h-5" />
                            </div>
                            <div>
                               <div className="text-sm text-muted-foreground font-mono uppercase">Quests Completed</div>
                               <div className="text-2xl font-bold text-white">843,921</div>
                            </div>
                         </div>
                      </div>

                      <div className="p-4 rounded-xl bg-gradient-to-r from-primary/20 to-transparent border border-primary/20">
                          <div className="text-sm text-primary font-mono mb-1">CURRENT SEASON</div>
                          <div className="text-xl font-bold text-white">Season 1: Awakening</div>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </section>


      </main>

      {/* Footer */}
      <footer className="border-t border-primary/10 py-12 bg-black/80 backdrop-blur-sm relative z-10">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4 opacity-50 hover:opacity-100 transition-opacity">
            <Sword className="w-5 h-5 text-primary" />
            <span className="font-bold text-lg text-primary font-mono">HigherMe</span>
          </div>
          <p className="text-xs text-muted-foreground font-mono">
             PRESS START TO BEGIN. © {new Date().getFullYear()}.
          </p>
        </div>
      </footer>
    </div>
  );
}
