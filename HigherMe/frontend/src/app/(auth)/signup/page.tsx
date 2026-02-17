'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';
import { Leaf, ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';

export default function SignUpPage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, register } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Simulate signup delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    await register(name, email, password);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-primary/5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/3 left-1/4 w-72 h-72 bg-secondary/10 rounded-full blur-3xl"></div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="mb-8 text-center">
          <Link href="/" className="inline-flex items-center space-x-2 mb-6 group">
            <div className="bg-primary/10 p-2 rounded-full group-hover:bg-primary/20 transition-colors">
              <Leaf className="w-6 h-6 text-primary" />
            </div>
            <span className="font-bold text-2xl text-primary">HigherMe</span>
          </Link>
        </div>

        <Card className="border-primary/10 shadow-2xl shadow-primary/5">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center">Start Growing</CardTitle>
            <CardDescription className="text-center text-muted-foreground">
              Create your account to unlock your potential
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="name" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  Full Name
                </label>
                <Input
                  id="name"
                  type="text"
                  placeholder="John Doe"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="bg-white/50 border-primary/20 focus:border-primary focus:ring-primary/20"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="email" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  Email
                </label>
                <Input
                  id="email"
                  type="email"
                  placeholder="name@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-white/50 border-primary/20 focus:border-primary focus:ring-primary/20"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="password" className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                  Password
                </label>
                <Input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-white/50 border-primary/20 focus:border-primary focus:ring-primary/20"
                  required
                />
                <p className="text-xs text-muted-foreground">
                  Must be at least 8 characters long
                </p>
              </div>
              <Button 
                type="submit" 
                className="w-full font-bold"
                variant="lush"
                disabled={isLoading}
              >
                {isLoading ? (
                  <span className="flex items-center gap-2">
                    <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"/>
                    Creating Account...
                  </span>
                ) : "Create Account"}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <div className="text-center text-sm text-muted-foreground">
              By clicking create account, you agree to our{' '}
              <Link href="#" className="underline hover:text-primary">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="#" className="underline hover:text-primary">
                Privacy Policy
              </Link>
              .
            </div>
            <div className="relative w-full">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t border-primary/10" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-muted-foreground font-medium">
                  Or sign up with
                </span>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 w-full">
              <Button variant="outline" className="w-full hover:bg-secondary/10 border-primary/20">
                Github
              </Button>
              <Button variant="outline" className="w-full hover:bg-secondary/10 border-primary/20">
                Google
              </Button>
            </div>
            <div className="text-center text-sm text-muted-foreground mt-4">
              Already have an account?{' '}
              <Link href="/signin" className="font-semibold text-primary hover:underline hover:text-primary/80">
                Sign in
              </Link>
            </div>
          </CardFooter>
        </Card>
        
        <div className="mt-8 text-center">
          <Link href="/" className="text-sm text-muted-foreground hover:text-primary flex items-center justify-center gap-2 transition-colors">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
        </div>
      </motion.div>
    </div>
  );
}
