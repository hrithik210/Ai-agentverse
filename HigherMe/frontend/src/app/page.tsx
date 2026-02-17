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

      {/* Header - Premium Grounded Look */}
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
            <Link href="#features" className="hover:text-primary transition-colors">Neural Sync</Link>
            <Link href="#metrics" className="hover:text-primary transition-colors">Biometrics</Link>
            <Link href="#code" className="hover:text-primary transition-colors">Contribution</Link>
          </nav>

          <div className="flex items-center gap-4">
            <Link href="/signin">
              <Button variant="ghost" className="text-sm font-medium text-muted-foreground hover:text-white hover:bg-white/5">
                Log In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="lush" className="text-sm font-semibold h-10 px-6 shadow-none hover:shadow-[0_0_20px_-5px_var(--primary)] text-black">
                Initialize
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 pt-24 relative z-10" ref={heroRef}>
        {/* Hero Section */}
        <section className="container mx-auto px-4 py-24 lg:py-32 text-center">
          <div className="max-w-4xl mx-auto space-y-8">
            <div className="hero-text inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-primary/80 text-xs font-mono tracking-wider backdrop-blur-md">
              <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></span>
              SYSTEM OPTIMIZED v2.0
            </div>
            
            <h1 className="hero-text text-5xl lg:text-7xl font-bold tracking-tight text-white leading-[1.1]">
              Engineered for <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-white/50">
                Peak Human Performance
              </span>
            </h1>
            
            <p className="hero-text text-lg text-muted-foreground/80 max-w-2xl mx-auto leading-relaxed font-light">
              A bioluminescent ecosystem to track your mental state, physical metrics, and code velocity. Calibrate your daily output with precision.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-10">
              <Link href="/signup" className="hero-btn">
                <Button variant="lush" size="lg" className="rounded-xl px-12 h-14 text-base font-semibold text-black tracking-wide border-2 border-transparent hover:border-white/20 transition-all duration-300">
                  Deploy System
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
              <Link href="#features" className="hero-btn">
                <Button variant="outline" size="lg" className="rounded-xl px-10 h-14 text-base border-white/10 bg-white/5 hover:bg-white/10 hover:text-white backdrop-blur-md text-muted-foreground">
                  View Protocol
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Premium High-Tech Grid (Formerly Features) */}
        <section id="features" className="container mx-auto px-4 py-32">
          <div className="grid md:grid-cols-3 gap-6 max-w-7xl mx-auto">
            {/* Card 1 */}
            <div className="feature-card group relative overflow-hidden rounded-3xl border border-white/5 bg-[#0C1F12]/40 p-8 backdrop-blur-sm lg:col-span-2 hover:border-primary/20 transition-colors duration-500">
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10 flex flex-col h-full justify-between">
                <div className="space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
                    <Zap className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="text-2xl font-semibold text-white">Neural State Tracking</h3>
                  <p className="text-muted-foreground max-w-md leading-relaxed">
                    Log cognitive load and emotional variance. Our system visualizes your mental patterns to optimize focused work sessions.
                  </p>
                </div>
                <div className="mt-8 h-32 w-full rounded-xl border border-white/5 bg-black/20 overflow-hidden relative">
                   {/* Abstract Viz */}
                   <div className="absolute inset-0 flex items-center justify-center gap-1 opacity-50">
                     {[...Array(20)].map((_, i) => (
                       <div key={i} className="w-1 bg-primary/40 rounded-full" style={{ height: `${Math.random() * 100}%` }} />
                     ))}
                   </div>
                </div>
              </div>
            </div>

            {/* Card 2 */}
             <div className="feature-card group relative overflow-hidden rounded-3xl border border-white/5 bg-[#0C1F12]/40 p-8 backdrop-blur-sm hover:border-primary/20 transition-colors duration-500">
               <div className="absolute inset-0 bg-gradient-to-bl from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
               <div className="relative z-10 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
                    <Target className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold text-white">Bio-Metrics</h3>
                  <p className="text-muted-foreground leading-relaxed text-sm">
                    Sync physical health data. Sleep quality and nutrition directly impact code quality.
                  </p>
                  <div className="pt-4 flex items-center gap-3">
                    <div className="h-2 flex-1 rounded-full bg-white/10 overflow-hidden">
                      <div className="h-full w-[85%] bg-primary rounded-full shadow-[0_0_10px_var(--primary)]" />
                    </div>
                    <span className="text-xs font-mono text-primary">85% OPTIMAL</span>
                  </div>
               </div>
             </div>

             {/* Card 3 */}
             <div className="feature-card group relative overflow-hidden rounded-3xl border border-white/5 bg-[#0C1F12]/40 p-8 backdrop-blur-sm hover:border-primary/20 transition-colors duration-500">
               <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
               <div className="relative z-10 space-y-4">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
                    <Code className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="text-xl font-semibold text-white">Commit Velocity</h3>
                  <p className="text-muted-foreground leading-relaxed text-sm">
                    Visualize contribution momentum. Maintain streaks to unlock flow state analytics.
                  </p>
               </div>
             </div>

             {/* Card 4 */}
             <div className="feature-card group relative overflow-hidden rounded-3xl border border-white/5 bg-[#0C1F12]/40 p-8 backdrop-blur-sm lg:col-span-2 hover:border-primary/20 transition-colors duration-500">
              <div className="absolute inset-0 bg-gradient-to-tl from-primary/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10 flex flex-col md:flex-row items-center gap-8">
                <div className="space-y-4 flex-1">
                  <div className="w-12 h-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
                    <Shield className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="text-2xl font-semibold text-white">System Architecture</h3>
                  <p className="text-muted-foreground leading-relaxed">
                     Built on a secure, high-performance foundation. Your data is encrypted and processed locally where possible.
                  </p>
                </div>
                <div className="w-full md:w-48 h-24 rounded-xl border border-white/5 bg-black/40 flex items-center justify-center font-mono text-xs text-primary/60">
                  <span className="animate-pulse">ENCRYPTION: ACTIVE</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Level Up Section (Social Proof) */}
        <section className="container mx-auto px-4 py-24 pb-40">
          <div className="max-w-5xl mx-auto bg-gradient-to-b from-[#0C1F12] to-black border border-primary/20 rounded-[2.5rem] p-12 text-center relative overflow-hidden shadow-[0_0_50px_rgba(74,222,128,0.1)]">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10"></div>
            
            <div className="inline-block mb-6 animate-bounce">
               <span className="text-6xl">🏆</span>
            </div>

            <h2 className="text-4xl lg:text-6xl font-black mb-12 relative z-10 text-white font-mono uppercase tracking-tighter">
              Ready to <span className="text-primary">Min-Max</span> Your Life?
            </h2>
            
            <div className="grid md:grid-cols-3 gap-12 text-center relative z-10 mb-12 border-t border-white/10 pt-12">
              <div className="space-y-2">
                <div className="text-5xl font-black font-mono text-primary">Lvl. 99</div>
                <div className="text-white/40 uppercase tracking-widest text-xs font-bold">Max Cap</div>
              </div>
              <div className="space-y-2">
                <div className="text-5xl font-black font-mono text-primary">100%</div>
                <div className="text-white/40 uppercase tracking-widest text-xs font-bold">Quest Completion</div>
              </div>
              <div className="space-y-2">
                <div className="text-5xl font-black font-mono text-primary">9000+</div>
                <div className="text-white/40 uppercase tracking-widest text-xs font-bold">XP Gained</div>
              </div>
            </div>
            
            <Link href="/signup" className="relative z-10 inline-block group">
              <Button size="lg" className="bg-primary text-black hover:bg-white hover:text-black rounded-xl px-16 h-20 text-2xl font-black shadow-[0_0_20px_rgba(74,222,128,0.5)] group-hover:shadow-[0_0_40px_rgba(255,255,255,0.5)] hover:scale-105 transition-all duration-300">
                JOIN THE SERVER
              </Button>
            </Link>
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
             PRESS START TO BEGIN. © {new Date().getFullYear()} SIDE PROJECT STUDIOS.
          </p>
        </div>
      </footer>
    </div>
  );
}
