'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ArrowRight, Code, Flame, Leaf, Scroll, Shield, Sword, Target, Zap } from 'lucide-react';
import gsap from 'gsap';

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
  const pageRef = useRef<HTMLDivElement>(null);
  const heroMediaRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const ctx = gsap.context(() => {
      if (prefersReducedMotion) {
        gsap.set('.hero-copy-item, .hero-cta, .hero-media-shell, .reveal-card, .verdict-item', {
          opacity: 1,
          y: 0,
          x: 0,
          scale: 1,
        });
        return;
      }

      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
      tl.from('.hero-copy-item', {
        y: 24,
        opacity: 0,
        duration: 0.75,
        stagger: 0.09,
      })
        .from(
          '.hero-cta',
          {
            y: 16,
            opacity: 0,
            duration: 0.5,
            stagger: 0.08,
          },
          '-=0.35'
        )
        .from(
          '.hero-media-shell',
          {
            x: 22,
            opacity: 0,
            duration: 0.7,
          },
          '-=0.35'
        )
        .from(
          '.hero-media-chip',
          {
            y: 18,
            opacity: 0,
            duration: 0.45,
            stagger: 0.07,
          },
          '-=0.4'
        )
        .from(
          '.reveal-card',
          {
            y: 26,
            opacity: 0,
            duration: 0.6,
            stagger: 0.08,
          },
          '-=0.15'
        )
        .from(
          '.verdict-item',
          {
            x: 18,
            opacity: 0,
            duration: 0.5,
            stagger: 0.06,
          },
          '-=0.2'
        );

      gsap.to(heroMediaRef.current, {
        y: -8,
        duration: 2.8,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      });
      gsap.to('.hero-scanline', {
        yPercent: 65,
        duration: 3.8,
        repeat: -1,
        ease: 'none',
      });
      gsap.to('.hero-data-track', {
        xPercent: -48,
        duration: 5.4,
        repeat: -1,
        ease: 'none',
      });
      gsap.to('.hero-pulse-ring', {
        scale: 1.12,
        opacity: 0.35,
        duration: 1.6,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      });
      gsap.to('.hero-orb', {
        scale: 1.08,
        duration: 1.6,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
      });
    }, pageRef);

    return () => ctx.revert();
  }, []);

  return (
    <div
      ref={pageRef}
      className="relative flex min-h-screen flex-col overflow-hidden bg-[#040A07] text-foreground selection:bg-primary/30 selection:text-primary-foreground"
    >
      <div className="pointer-events-none absolute inset-0 z-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_16%,rgba(74,222,128,0.18),transparent_34%),radial-gradient(circle_at_84%_12%,rgba(34,197,94,0.12),transparent_36%),linear-gradient(145deg,#040A07_5%,#09150E_45%,#040A07_100%)]" />
        <div className="absolute inset-0 opacity-[0.06] [background:repeating-linear-gradient(0deg,transparent,transparent_18px,rgba(255,255,255,0.6)_19px)]" />
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
        <section className="container mx-auto px-4 pb-14 pt-12 lg:pb-16 lg:pt-16">
          <div className="grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:gap-12">
            <div className="order-1">
              <div className="hero-copy-item inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-xs font-bold uppercase tracking-[0.18em] text-primary">
                <span className="h-2 w-2 rounded-full bg-primary animate-pulse" />
                System Online
              </div>

              <h1 className="hero-copy-item mt-5 text-4xl font-black leading-[1.03] tracking-tight text-white sm:text-5xl lg:text-6xl xl:text-7xl">
                Your Solo Leveling System
                <span className="mt-2 block bg-gradient-to-r from-primary via-[#86EFAC] to-primary bg-clip-text text-transparent">
                  with Daily AI Judgment
                </span>
              </h1>

              <p className="hero-copy-item mt-5 max-w-xl text-base leading-relaxed text-muted-foreground sm:text-lg lg:text-xl">
                Track coding, mood, meals, sleep, and water in one place. At the end of the day, HigherMe tells you
                what improved, what slipped, and what to fix tomorrow.
              </p>

              <p className="hero-copy-item mt-4 max-w-lg text-sm text-white/65 sm:text-base">
                Built for solo builders who want structure without excuses.
              </p>

              <div className="mt-7 flex flex-col items-start gap-3 sm:flex-row sm:items-center">
                <Link href="/signup" className="hero-cta">
                  <Button
                    variant="lush"
                    size="lg"
                    className="h-14 rounded-xl border border-primary/50 px-9 text-lg font-bold shadow-[0_0_24px_rgba(74,222,128,0.32)]"
                  >
                    <Flame className="mr-2 h-5 w-5 fill-current" />
                    Start Leveling
                  </Button>
                </Link>
                <Link href="#systems" className="hero-cta">
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

            <div className="hero-media-shell order-2">
              <article
                ref={heroMediaRef}
                className="hero-video-shell relative overflow-hidden rounded-[1.8rem] border border-white/10 bg-[linear-gradient(160deg,rgba(12,31,18,0.95)_0%,rgba(8,17,12,0.92)_50%,rgba(7,15,11,0.98)_100%)] p-3 shadow-[0_24px_100px_-35px_rgba(0,0,0,0.9)]"
              >
                <div className="relative overflow-hidden rounded-[1.25rem] border border-white/10 bg-black/40 p-5 sm:p-6">
                  <div className="hero-video-noise pointer-events-none absolute inset-0" />
                  <div className="hero-video-vignette pointer-events-none absolute inset-0" />
                  <div className="hero-scanline pointer-events-none absolute inset-x-0 -top-[58%] h-[175%]" />
                  <div className="hero-pulse-ring pointer-events-none absolute left-1/2 top-[54%] h-44 w-44 -translate-x-1/2 -translate-y-1/2 rounded-full border border-primary/35 opacity-20" />
                  <div className="hero-orb pointer-events-none absolute left-1/2 top-[54%] h-3 w-3 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary/80 shadow-[0_0_22px_rgba(74,222,128,0.8)]" />

                  <div className="relative z-10 mb-5 flex items-center justify-between">
                    <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-400/10 px-2.5 py-1 text-[11px] font-mono uppercase tracking-[0.12em] text-emerald-300">
                      <span className="h-2 w-2 rounded-full bg-emerald-300" />
                      Live Session
                    </div>
                    <div className="text-xs font-mono text-white/60">Today 21:14</div>
                  </div>

                  <div className="relative z-10 grid gap-3">
                    <div className="hero-media-chip rounded-xl border border-white/10 bg-white/5 p-3">
                      <div className="mb-2 flex items-center justify-between text-[11px] font-mono uppercase tracking-[0.12em] text-white/55">
                        <span>Current Level</span>
                        <span>Lv 07</span>
                      </div>
                      <div className="h-2 overflow-hidden rounded-full bg-black/50">
                        <div className="h-full w-[72%] rounded-full bg-gradient-to-r from-primary via-emerald-300 to-primary" />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div className="hero-media-chip rounded-xl border border-white/10 bg-white/5 p-3">
                        <div className="text-[10px] font-mono uppercase tracking-[0.12em] text-white/55">Hydration</div>
                        <div className="mt-1 text-lg font-bold text-white">78%</div>
                      </div>
                      <div className="hero-media-chip rounded-xl border border-white/10 bg-white/5 p-3">
                        <div className="text-[10px] font-mono uppercase tracking-[0.12em] text-white/55">Mood</div>
                        <div className="mt-1 text-lg font-bold text-white">Stable</div>
                      </div>
                    </div>

                    <div className="hero-media-chip rounded-xl border border-primary/20 bg-gradient-to-r from-primary/20 to-transparent p-3">
                      <div className="text-[10px] font-mono uppercase tracking-[0.12em] text-primary">AI Verdict</div>
                      <div className="mt-1 text-sm font-semibold text-white">Good consistency. Increase deep work block tomorrow.</div>
                    </div>

                    <div className="hero-media-chip overflow-hidden rounded-xl border border-white/10 bg-black/40">
                      <div className="hero-data-track h-8 w-[190%]" />
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section id="systems" className="container mx-auto px-4 pb-16 pt-1 lg:pb-20 lg:pt-3">
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
