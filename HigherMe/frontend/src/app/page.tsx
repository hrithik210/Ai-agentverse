'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { ArrowRight, Zap, Target, Code, CheckCircle, BarChart3, Shield } from 'lucide-react';

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Header */}
      <header className="fixed top-0 w-full bg-background/80 backdrop-blur-md z-50 border-b border-border/40">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Zap className="w-6 h-6 text-primary" />
            <span className="font-bold text-xl tracking-tight">HigherMe</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link href="/signin">
              <Button variant="ghost" className="text-sm font-medium">
                Sign In
              </Button>
            </Link>
            <Link href="/signup">
              <Button className="premium-button text-sm">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main className="flex-1 pt-24">
        {/* Hero Section */}
        <section className="container mx-auto px-4 py-20 lg:py-32 text-center">
          <motion.div
            initial="initial"
            animate="animate"
            variants={staggerContainer}
            className="max-w-4xl mx-auto space-y-8"
          >
            <motion.div variants={fadeIn}>
              <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-sm font-semibold mb-6">
                v2.0 Now Available
              </span>
              <h1 className="text-5xl lg:text-7xl font-bold tracking-tight text-foreground leading-[1.1]">
                Level up your life with <span className="text-primary">precision</span>
              </h1>
            </motion.div>
            
            <motion.p 
              variants={fadeIn}
              className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed"
            >
              The ultimate solo leveling system for developers. Track your mood, optimize your health, and accelerate your coding progress with data-driven insights.
            </motion.p>
            
            <motion.div 
              variants={fadeIn}
              className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4"
            >
              <Link href="/signup">
                <Button size="lg" className="premium-button h-12 px-8 text-base">
                  Start Leveling Up
                  <ArrowRight className="ml-2 w-4 h-4" />
                </Button>
              </Link>
              <Link href="#features">
                <Button variant="outline" size="lg" className="h-12 px-8 text-base bg-background/50 hover:bg-muted/50">
                  View Features
                </Button>
              </Link>
            </motion.div>
          </motion.div>
        </section>

        {/* Features Grid */}
        <section id="features" className="container mx-auto px-4 py-24 bg-muted/30">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Everything you need to grow</h2>
            <p className="text-muted-foreground text-lg">
              A complete system designed to help you become the best version of yourself.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {[
              {
                icon: <Target className="w-10 h-10 text-blue-500" />,
                title: "Mood Tracking",
                description: "Monitor your mental state with daily check-ins and identify patterns that affect your productivity."
              },
              {
                icon: <BarChart3 className="w-10 h-10 text-indigo-500" />,
                title: "Health Logging",
                description: "Keep track of your meals, exercise, and sleep to ensure your physical engine is running at peak performance."
              },
              {
                icon: <Code className="w-10 h-10 text-violet-500" />,
                title: "Code Progress",
                description: "Visualize your coding activity and Github contributions to maintain your streak and momentum."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-card p-8 rounded-2xl shadow-sm border border-border/50 hover:shadow-md transition-all duration-300"
              >
                <div className="mb-6 p-4 bg-primary/5 rounded-xl w-fit">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Social Proof / Trust */}
        <section className="container mx-auto px-4 py-24">
          <div className="max-w-5xl mx-auto bg-primary text-primary-foreground rounded-3xl p-12 text-center relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-full bg-[linear-gradient(45deg,rgba(255,255,255,0.1)_25%,transparent_25%,transparent_50%,rgba(255,255,255,0.1)_50%,rgba(255,255,255,0.1)_75%,transparent_75%,transparent)] bg-[length:64px_64px] opacity-10"></div>
            
            <h2 className="text-3xl lg:text-4xl font-bold mb-8 relative z-10">Ready to start your journey?</h2>
            <div className="grid md:grid-cols-3 gap-8 text-center relative z-10 mb-10">
              <div className="space-y-2">
                <div className="text-4xl font-bold">100%</div>
                <div className="text-primary-foreground/80">Focus</div>
              </div>
              <div className="space-y-2">
                <div className="text-4xl font-bold">24/7</div>
                <div className="text-primary-foreground/80">Uptime</div>
              </div>
              <div className="space-y-2">
                <div className="text-4xl font-bold">Level 99</div>
                <div className="text-primary-foreground/80">Potential</div>
              </div>
            </div>
            
            <Link href="/signup">
              <Button size="lg" variant="secondary" className="px-8 h-12 text-primary font-bold shadow-lg hover:shadow-xl transition-all">
                Join Now Free
              </Button>
            </Link>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-border/40 py-12 bg-muted/20">
        <div className="container mx-auto px-4 grid md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Zap className="w-5 h-5 text-primary" />
              <span className="font-bold text-lg">HigherMe</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Empowering developers to achieve their peak potential through data-driven self-improvement.
            </p>
          </div>
          <div>
            <h4 className="font-bold mb-4">Product</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="#" className="hover:text-primary">Features</Link></li>
              <li><Link href="#" className="hover:text-primary">Pricing</Link></li>
              <li><Link href="#" className="hover:text-primary">Changelog</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Company</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="#" className="hover:text-primary">About</Link></li>
              <li><Link href="#" className="hover:text-primary">Blog</Link></li>
              <li><Link href="#" className="hover:text-primary">Careers</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><Link href="#" className="hover:text-primary">Privacy</Link></li>
              <li><Link href="#" className="hover:text-primary">Terms</Link></li>
            </ul>
          </div>
        </div>
        <div className="container mx-auto px-4 mt-12 pt-8 border-t border-border/40 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} HigherMe. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
