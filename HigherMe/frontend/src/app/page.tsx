'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { useAuth } from '@/hooks/useAuth';
import { Zap, TrendingUp, Target, Code, Heart, Brain } from 'lucide-react';

export default function LandingPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const { login, register, user } = useAuth();
  const router = useRouter();

  // Redirect to dashboard if already authenticated
  useEffect(() => {
    if (user) {
      router.push('/dashboard');
    }
  }, [user, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (isLogin) {
        await login(formData.email, formData.password);
      } else {
        await register(formData.username, formData.email, formData.password);
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-6xl mx-auto grid lg:grid-cols-2 gap-8 items-center">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="space-y-8"
        >
          <div className="space-y-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="flex items-center space-x-2"
            >
              <Zap className="w-10 h-10 text-blue-400" />
              <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                HigherMe
              </h1>
            </motion.div>
            
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="text-xl text-gray-300 leading-relaxed"
            >
              Level up your life with the ultimate solo leveling system. Track your mood, health, and coding progress to unlock your true potential.
            </motion.p>
          </div>

          {/* Features */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.6 }}
            className="grid grid-cols-1 sm:grid-cols-3 gap-4"
          >
            <div className="glass-effect p-4 rounded-lg">
              <Brain className="w-8 h-8 text-blue-400 mb-2" />
              <h3 className="font-semibold text-white">Mood Tracking</h3>
              <p className="text-sm text-gray-400">Monitor your mental state</p>
            </div>
            <div className="glass-effect p-4 rounded-lg">
              <Heart className="w-8 h-8 text-red-400 mb-2" />
              <h3 className="font-semibold text-white">Health Logging</h3>
              <p className="text-sm text-gray-400">Track meals, exercise & sleep</p>
            </div>
            <div className="glass-effect p-4 rounded-lg">
              <Code className="w-8 h-8 text-green-400 mb-2" />
              <h3 className="font-semibold text-white">Code Progress</h3>
              <p className="text-sm text-gray-400">Monitor coding activity</p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
            className="flex items-center space-x-4 text-sm text-gray-400"
          >
            <div className="flex items-center space-x-1">
              <TrendingUp className="w-4 h-4" />
              <span>Real-time XP tracking</span>
            </div>
            <div className="flex items-center space-x-1">
              <Target className="w-4 h-4" />
              <span>Achievement system</span>
            </div>
          </motion.div>
        </motion.div>

        {/* Auth Form */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="w-full max-w-md mx-auto"
        >
          <Card className="neon-border">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">
                {isLogin ? 'Welcome Back' : 'Join HigherMe'}
              </CardTitle>
              <CardDescription>
                {isLogin 
                  ? 'Continue your leveling journey' 
                  : 'Start your solo leveling adventure'
                }
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                {!isLogin && (
                  <div>
                    <Input
                      name="username"
                      type="text"
                      placeholder="Choose a username"
                      value={formData.username}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                )}
                
                <div>
                  <Input
                    name="email"
                    type="email"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>
                
                <div>
                  <Input
                    name="password"
                    type="password"
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                {error && (
                  <div className="text-red-400 text-sm text-center bg-red-900/20 p-2 rounded">
                    {error}
                  </div>
                )}

                <Button
                  type="submit"
                  className="w-full"
                  disabled={isLoading}
                >
                  {isLoading ? 'Loading...' : (isLogin ? 'Sign In' : 'Create Account')}
                </Button>
              </form>

              <div className="mt-6 text-center">
                <button
                  type="button"
                  onClick={() => setIsLogin(!isLogin)}
                  className="text-blue-400 hover:text-blue-300 text-sm"
                >
                  {isLogin 
                    ? "Don't have an account? Sign up" 
                    : 'Already have an account? Sign in'
                  }
                </button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  );
}
