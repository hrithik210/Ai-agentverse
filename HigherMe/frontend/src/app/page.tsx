'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ArrowRight, Zap, Target, Code, BarChart3, Leaf, Wind } from 'lucide-react';
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
        y: 100,
        opacity: 0,
        duration: 1,
        stagger: 0.2
      })
      .from(".hero-btn", {
        y: 20,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1
      }, "-=0.5")
      .from(".feature-card", {
        y: 50,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1
      }, "-=0.5");
    }, heroRef);

    // Three.js Background
    if (!canvasRef.current) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ 
      canvas: canvasRef.current, 
      alpha: true,
      antialias: true 
    });

    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Create Organic Particles (Leaves/Orbs)
    const geometry = new THREE.IcosahedronGeometry(0.5, 0);
    const material = new THREE.MeshBasicMaterial({ 
      color: 0x68BA7F,
      transparent: true,
      opacity: 0.3,
      wireframe: true
    });

    const particles: THREE.Mesh[] = [];
    for (let i = 0; i < 50; i++) {
      const particle = new THREE.Mesh(geometry, material);
      particle.position.set(
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20
      );
      scene.add(particle);
      particles.push(particle);
    }

    camera.position.z = 10;

    // Mouse Interaction
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

      particles.forEach((particle, i) => {
        particle.rotation.x += 0.002;
        particle.rotation.y += 0.003;
        
        // Float effect
        particle.position.y += Math.sin(Date.now() * 0.001 + i) * 0.01;
        
        // Mouse influence
        particle.position.x += (mouseX * 0.5 - particle.position.x) * 0.02;
        particle.position.y += (mouseY * 0.5 - particle.position.y) * 0.02;
      });

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
      // Cleanup Three.js
      particles.forEach(p => {
        p.geometry.dispose();
        (p.material as THREE.Material).dispose();
      });
      renderer.dispose();
    };
  }, []);

  return (
    <div className="min-h-screen bg-transparent text-foreground flex flex-col relative overflow-hidden">
      {/* 3D Background Canvas */}
      <canvas 
        ref={canvasRef} 
        className="fixed top-0 left-0 w-full h-full pointer-events-none z-0"
      />

      {/* Header */}
      <header className="fixed top-0 w-full lush-glass z-50">
        <div className="container mx-auto px-4 h-20 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Leaf className="w-8 h-8 text-primary" />
            <span className="font-bold text-2xl tracking-tight text-primary">HigherMe</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/signin">
              <Button variant="ghost" className="text-sm font-medium hover:text-primary">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="lush" className="text-sm font-medium">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 pt-24 relative z-10" ref={heroRef}>
        {/* Hero Section */}
        <section className="container mx-auto px-4 py-24 lg:py-32 text-center">
          <div className="max-w-5xl mx-auto space-y-8">
            <div className="hero-text inline-block px-4 py-1.5 rounded-full bg-secondary/20 text-primary text-sm font-semibold border border-secondary/30 backdrop-blur-sm">
              <span className="flex items-center gap-2">
                <Wind className="w-4 h-4" />
                Waitlist 2.0 Open
              </span>
            </div>
            
            <h1 className="hero-text text-6xl lg:text-8xl font-bold tracking-tight text-primary leading-[1.1]">
              Cultivate Your <br/>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#2E6F40] to-[#68BA7F]">
                Potential
              </span>
            </h1>
            
            <p className="hero-text text-xl lg:text-2xl text-muted-foreground/80 max-w-2xl mx-auto leading-relaxed font-light">
              The organic AI ecosystem for personal growth. Monitor your mental state, health, and code with precision.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8">
              <Link href="/signup" className="hero-btn">
                <Button variant="lush" size="lg" className="rounded-full px-10 h-14 text-lg">
                  Start Growing
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <Link href="#features" className="hero-btn">
                <Button variant="outline" size="lg" className="rounded-full px-10 h-14 text-lg border-primary/30 hover:bg-primary/5">
                  Explore Ecosystem
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="container mx-auto px-4 py-32">
          <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {[
              {
                icon: <Target className="w-10 h-10 text-primary" />,
                title: "Mood Tracking",
                description: "Daily check-ins to monitor your mental ecosystem."
              },
              {
                icon: <BarChart3 className="w-10 h-10 text-primary" />,
                title: "Health Logging",
                description: "Optimize your physical engine for peak performance."
              },
              {
                icon: <Code className="w-10 h-10 text-primary" />,
                title: "Code Progress",
                description: "Visualize your contribution graph like a growing forest."
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="feature-card lush-glass p-8 rounded-3xl lush-card-hover group relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 p-8 opacity-10 group-hover:scale-110 transition-transform duration-500">
                  {feature.icon}
                </div>
                <div className="mb-6 p-4 bg-secondary/20 rounded-2xl w-fit text-primary">
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-primary">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Social Proof */}
        <section className="container mx-auto px-4 py-24 pb-40">
          <div className="max-w-5xl mx-auto bg-gradient-to-br from-primary to-[#1a4a2a] text-white rounded-[2.5rem] p-12 text-center relative overflow-hidden shadow-2xl">
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>
            
            <h2 className="text-4xl lg:text-5xl font-bold mb-12 relative z-10">Thrive in the Digital Age</h2>
            
            <div className="grid md:grid-cols-3 gap-12 text-center relative z-10 mb-12 border-t border-white/10 pt-12">
              <div className="space-y-2">
                <div className="text-5xl font-bold font-mono">100%</div>
                <div className="text-white/60 uppercase tracking-widest text-sm">Organic Growth</div>
              </div>
              <div className="space-y-2">
                <div className="text-5xl font-bold font-mono">24/7</div>
                <div className="text-white/60 uppercase tracking-widest text-sm">System Uptime</div>
              </div>
              <div className="space-y-2">
                <div className="text-5xl font-bold font-mono">Lvl.99</div>
                <div className="text-white/60 uppercase tracking-widest text-sm">Max Potential</div>
              </div>
            </div>
            
            <Link href="/signup" className="relative z-10 inline-block">
              <Button size="lg" className="bg-[#CFFFDC] text-primary hover:bg-white rounded-full px-12 h-16 text-lg font-bold shadow-xl hover:scale-105 transition-all duration-300">
                Join the Ecosystem
              </Button>
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-primary/10 py-12 bg-white/50 backdrop-blur-sm relative z-10">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Leaf className="w-6 h-6 text-primary" />
            <span className="font-bold text-xl text-primary">HigherMe</span>
          </div>
          <p className="text-sm text-muted-foreground">
            © {new Date().getFullYear()} HigherMe Ecosystem. Cultivated with precision.
          </p>
        </div>
      </footer>
    </div>
  );
}
