'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import {
  ArrowRight,
  Code,
  Flame,
  Leaf,
  Scroll,
  Shield,
  Sword,
  Target,
  Zap,
} from 'lucide-react';
import gsap from 'gsap';
import * as THREE from 'three';

const corePillars = [
  {
    icon: <Target className="h-9 w-9 text-primary" />,
    stat: '+INT',
    title: 'Mood Tracking',
    description:
      'Log mood swings as they happen. Spot emotional patterns before they start controlling your day.',
  },
  {
    icon: <Shield className="h-9 w-9 text-primary" />,
    stat: '+VIT',
    title: 'Health Logging',
    description:
      'Track meals, water, sleep, and exercise in one place so your baseline stays stable while you work.',
  },
  {
    icon: <Code className="h-9 w-9 text-primary" />,
    stat: '+DEX',
    title: 'Coding Progress',
    description:
      'Measure your coding momentum with your current VS Code activity signal and keep a real streak.',
  },
];

const verdictSignals = [
  {
    icon: <Zap className="h-5 w-5" />,
    label: 'Mood Trend',
    value: 'Up, stable, or drained',
  },
  {
    icon: <Scroll className="h-5 w-5" />,
    label: 'Habit Compliance',
    value: 'Meals, water, and sleep score',
  },
  {
    icon: <Sword className="h-5 w-5" />,
    label: 'Execution Score',
    value: 'Coding streak and momentum',
  },
];

export default function LandingPage() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const ctx = gsap.context(() => {
      if (prefersReducedMotion) {
        gsap.set('.hero-item, .hero-action, .reveal-card, .verdict-item', {
          opacity: 1,
          y: 0,
          scale: 1,
        });
        return;
      }

      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
      tl.from('.hero-item', {
        y: 24,
        opacity: 0,
        duration: 0.8,
        stagger: 0.1,
      })
        .from(
          '.hero-action',
          {
            y: 16,
            opacity: 0,
            duration: 0.55,
            stagger: 0.08,
          },
          '-=0.4'
        )
        .from(
          '.reveal-card',
          {
            y: 30,
            opacity: 0,
            duration: 0.6,
            stagger: 0.08,
          },
          '-=0.15'
        )
        .from(
          '.verdict-item',
          {
            x: 20,
            opacity: 0,
            duration: 0.5,
            stagger: 0.07,
          },
          '-=0.2'
        );
    }, pageRef);

    if (!canvasRef.current || prefersReducedMotion) {
      return () => ctx.revert();
    }

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050a06, 0.045);

    const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 10;

    const renderer = new THREE.WebGLRenderer({
      canvas: canvasRef.current,
      alpha: true,
      antialias: true,
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));

    const geometry = new THREE.BufferGeometry();
    const count = 130;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let index = 0; index < count; index++) {
      positions[index * 3] = (Math.random() - 0.5) * 24;
      positions[index * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[index * 3 + 2] = (Math.random() - 0.5) * 20;

      colors[index * 3] = 0.2 + Math.random() * 0.12;
      colors[index * 3 + 1] = 0.78 + Math.random() * 0.2;
      colors[index * 3 + 2] = 0.22 + Math.random() * 0.3;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 0.11,
      vertexColors: true,
      transparent: true,
      opacity: 0.55,
      blending: THREE.AdditiveBlending,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    let frameId = 0;
    let pointerTargetX = 0;
    let pointerTargetY = 0;
    let pointerX = 0;
    let pointerY = 0;

    const onPointerMove = (event: PointerEvent) => {
      pointerTargetX = (event.clientX / window.innerWidth) * 2 - 1;
      pointerTargetY = -(event.clientY / window.innerHeight) * 2 + 1;
    };

    const onResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    const animate = () => {
      frameId = window.requestAnimationFrame(animate);

      pointerX += (pointerTargetX - pointerX) * 0.035;
      pointerY += (pointerTargetY - pointerY) * 0.035;

      const time = performance.now() * 0.00035;
      particles.rotation.x = time * 0.07 + pointerY * 0.12;
      particles.rotation.y = time * 0.1 + pointerX * 0.12;
      material.size = 0.11 + Math.sin(time * 8) * 0.015;

      renderer.render(scene, camera);
    };

    window.addEventListener('pointermove', onPointerMove, { passive: true });
    window.addEventListener('resize', onResize);
    animate();

    return () => {
      ctx.revert();
      window.cancelAnimationFrame(frameId);
      window.removeEventListener('pointermove', onPointerMove);
      window.removeEventListener('resize', onResize);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div
      ref={pageRef}
      className="relative flex min-h-screen flex-col overflow-hidden bg-transparent text-foreground selection:bg-primary/30 selection:text-primary-foreground"
    >
      <canvas ref={canvasRef} className="pointer-events-none fixed inset-0 z-0 h-full w-full" />
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_18%_20%,rgba(74,222,128,0.12),transparent_38%),radial-gradient(circle_at_82%_85%,rgba(34,197,94,0.08),transparent_42%)]" />
        <div className="absolute -top-32 left-1/2 h-[26rem] w-[26rem] -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
      </div>

      <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-[#050A06]/80 backdrop-blur-xl supports-[backdrop-filter]:bg-[#050A06]/65">
        <div className="container mx-auto flex h-20 items-center justify-between px-4 sm:px-6">
          <Link href="/" className="group flex items-center gap-3">
            <div className="relative flex h-10 w-10 items-center justify-center overflow-hidden rounded-xl border border-primary/20 bg-gradient-to-tr from-primary/20 to-primary/5 transition-colors duration-500 group-hover:border-primary/50">
              <div className="absolute inset-0 bg-primary/20 opacity-0 blur-xl transition-opacity duration-500 group-hover:opacity-100" />
              <Leaf className="relative z-10 h-5 w-5 text-primary" />
            </div>
            <span className="text-xl font-bold tracking-tight text-white/90">HigherMe</span>
          </Link>

          <nav className="hidden items-center gap-7 text-sm font-medium text-muted-foreground md:flex">
            <Link href="#systems" className="transition-colors hover:text-primary">
              Systems
            </Link>
            <Link href="#verdict" className="transition-colors hover:text-primary">
              Verdict
            </Link>
            <Link href="#join" className="transition-colors hover:text-primary">
              Join
            </Link>
          </nav>

          <div className="flex items-center gap-2 sm:gap-3">
            <Link href="/signin">
              <Button variant="ghost" className="text-sm text-muted-foreground hover:bg-white/5 hover:text-white">
                Log In
              </Button>
            </Link>
            <Link href="/signup">
              <Button variant="lush" className="h-10 px-5 text-sm font-semibold text-black sm:px-6">
                Start Run
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="relative z-10 flex-1 pt-20">
        <section className="container mx-auto px-4 pb-10 pt-16 text-center lg:pb-12 lg:pt-20">
          <div className="mx-auto max-w-5xl space-y-6">
            <div className="hero-item inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-primary">
              <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
              System Online
            </div>

            <h1 className="hero-item text-4xl font-black leading-[1.02] tracking-tight text-white sm:text-5xl lg:text-7xl">
              Your Solo Leveling System
              <span className="mt-2 block bg-gradient-to-r from-primary via-[#86EFAC] to-primary bg-clip-text text-transparent">
                for Real Life Execution
              </span>
            </h1>

            <p className="hero-item mx-auto max-w-3xl text-base leading-relaxed text-muted-foreground sm:text-lg lg:text-xl">
              HigherMe helps you track coding, mood, meals, sleep, and water in one place, then gives you an AI
              end-of-day verdict so you know exactly what to improve tomorrow.
            </p>

            <p className="hero-item mx-auto max-w-2xl text-sm text-white/60 sm:text-base">
              Built like a personal judge for solo builders: fewer excuses, clearer feedback, stronger routines.
            </p>

            <div className="flex flex-col items-center justify-center gap-4 pt-5 sm:flex-row">
              <Link href="/signup" className="hero-action">
                <Button
                  variant="lush"
                  size="lg"
                  className="h-14 rounded-xl border border-primary/50 px-9 text-lg font-bold shadow-[0_0_24px_rgba(74,222,128,0.32)]"
                >
                  <Flame className="mr-2 h-5 w-5 fill-current" />
                  Start Leveling
                </Button>
              </Link>
              <Link href="#systems" className="hero-action">
                <Button
                  variant="outline"
                  size="lg"
                  className="h-14 rounded-xl border-white/15 bg-white/5 px-8 text-base text-gray-200 backdrop-blur-md hover:bg-white/10 hover:text-white"
                >
                  Explore Systems
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </section>

        <section id="systems" className="container mx-auto px-4 pb-16 pt-4 lg:pb-20 lg:pt-6">
          <div className="mx-auto max-w-6xl">
            <div className="mb-8 text-center">
              <p className="mb-3 text-xs font-semibold uppercase tracking-[0.18em] text-primary/90">Core Systems</p>
              <h2 className="text-3xl font-black tracking-tight text-white sm:text-4xl">Three pillars. One feedback loop.</h2>
            </div>

            <div className="grid gap-5 md:grid-cols-3">
              {corePillars.map((pillar) => (
                <article
                  key={pillar.title}
                  className="reveal-card group relative overflow-hidden rounded-3xl border border-white/5 bg-[rgba(12,31,18,0.64)] p-7 backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-primary/45"
                >
                  <div className="absolute right-4 top-4 rounded border border-primary/20 px-2 py-1 font-mono text-xs text-primary/90">
                    {pillar.stat}
                  </div>
                  <div className="mb-5 w-fit rounded-2xl bg-primary/10 p-3 text-primary ring-1 ring-primary/25 transition-colors duration-300 group-hover:bg-primary group-hover:text-black">
                    {pillar.icon}
                  </div>
                  <h3 className="mb-2 text-2xl font-bold text-white">{pillar.title}</h3>
                  <p className="text-sm leading-relaxed text-muted-foreground">{pillar.description}</p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section id="verdict" className="container mx-auto px-4 pb-24 lg:pb-28">
          <div className="relative mx-auto max-w-5xl overflow-hidden rounded-[2rem] border border-white/10 bg-[#0C1F12]/70 backdrop-blur-md">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_-20%,rgba(74,222,128,0.14),transparent_68%)]" />
            <div className="relative z-10 grid md:grid-cols-2">
              <div id="join" className="border-b border-white/5 p-8 md:border-b-0 md:border-r md:p-10 lg:p-12">
                <div className="mb-4 inline-flex items-center gap-2 rounded-md border border-primary/20 bg-primary/10 px-3 py-1 text-xs font-mono text-primary">
                  <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                  DAILY VERDICT ENGINE
                </div>
                <h2 className="mb-4 text-3xl font-black tracking-tight text-white sm:text-4xl lg:text-5xl">
                  Track today.
                  <br />
                  Improve tomorrow.
                </h2>
                <p className="mb-7 text-base leading-relaxed text-muted-foreground sm:text-lg">
                  At the end of your day, HigherMe summarizes your mood, habits, and coding output like a fair system
                  judge, so you can fix weak spots fast.
                </p>
                <div className="flex flex-col gap-3 sm:flex-row">
                  <Link href="/signup">
                    <Button className="h-12 px-7 text-base font-semibold">Create Account</Button>
                  </Link>
                  <Link href="/signin">
                    <Button variant="ghost" className="h-12 px-7 text-base text-white hover:bg-white/5">
                      Sign In
                    </Button>
                  </Link>
                </div>
              </div>

              <div className="bg-black/20 p-8 md:p-10 lg:p-12">
                <div className="space-y-4">
                  {verdictSignals.map((signal) => (
                    <div
                      key={signal.label}
                      className="verdict-item flex items-start justify-between gap-4 rounded-xl border border-white/5 bg-white/[0.03] p-4"
                    >
                      <div className="flex items-center gap-3">
                        <div className="rounded-full bg-primary/20 p-2 text-primary">{signal.icon}</div>
                        <div>
                          <div className="text-xs font-mono uppercase tracking-wider text-muted-foreground">{signal.label}</div>
                          <div className="text-sm font-semibold text-white">{signal.value}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="verdict-item mt-4 rounded-xl border border-primary/20 bg-gradient-to-r from-primary/20 to-transparent p-4">
                  <div className="text-xs font-mono uppercase tracking-wider text-primary">Current Status</div>
                  <div className="mt-1 text-lg font-bold text-white">Open Beta</div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="relative z-10 border-t border-primary/10 bg-black/70 py-10 backdrop-blur-sm">
        <div className="container mx-auto px-4 text-center">
          <div className="mb-3 flex items-center justify-center gap-2 opacity-75 transition-opacity hover:opacity-100">
            <Sword className="h-5 w-5 text-primary" />
            <span className="font-mono text-lg font-bold text-primary">HigherMe</span>
          </div>
          <p className="text-xs font-mono text-muted-foreground">
            Press start and build your baseline. © {new Date().getFullYear()}.
          </p>
        </div>
      </footer>
    </div>
  );
}
