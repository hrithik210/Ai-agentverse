'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '@/hooks/useAuth';
import { ApiClient } from '@/lib/api';
import { UserStats, DailyReport } from '@/types/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { 
  User, 
  Trophy, 
  Zap, 
  Heart, 
  Brain, 
  Code2, 
  Utensils, 
  Dumbbell, 
  Moon, 
  Droplets,
  LogOut,
  TrendingUp,
  Calendar,
  Activity
} from 'lucide-react';

interface LoggingModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water';
  onSubmit: (data: any) => void;
}

const LoggingModal = ({ isOpen, onClose, type, onSubmit }: LoggingModalProps) => {
  const [formData, setFormData] = useState<Record<string, any>>({});
  
  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
    onClose();
    setFormData({});
  };

  const renderForm = () => {
    switch (type) {
      case 'mood':
        return (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Mood Rating (1-10)
              </label>
              <Input
                type="number"
                min="1"
                max="10"
                value={formData.mood_rating || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, mood_rating: parseInt(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Energy Level (1-10)
              </label>
              <Input
                type="number"
                min="1"
                max="10"
                value={formData.energy_level || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, energy_level: parseInt(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Stress Level (1-10)
              </label>
              <Input
                type="number"
                min="1"
                max="10"
                value={formData.stress_level || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, stress_level: parseInt(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Notes (Optional)
              </label>
              <Input
                type="text"
                value={formData.notes || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                placeholder="How are you feeling today?"
              />
            </div>
          </>
        );
      
      case 'meal':
        return (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Calories
              </label>
              <Input
                type="number"
                value={formData.calories || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, calories: parseInt(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Description
              </label>
              <Input
                type="text"
                value={formData.description || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
                placeholder="What did you eat?"
                required
              />
            </div>
          </>
        );
      
      case 'exercise':
        return (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Duration (minutes)
              </label>
              <Input
                type="number"
                value={formData.duration_minutes || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, duration_minutes: parseInt(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Exercise Type
              </label>
              <Input
                type="text"
                value={formData.exercise_type || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, exercise_type: e.target.value }))}
                placeholder="Running, weightlifting, yoga..."
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Intensity (1-10)
              </label>
              <Input
                type="number"
                min="1"
                max="10"
                value={formData.intensity || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, intensity: parseInt(e.target.value) }))}
                required
              />
            </div>
          </>
        );
      
      case 'sleep':
        return (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Hours Slept
              </label>
              <Input
                type="number"
                step="0.5"
                value={formData.hours || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, hours: parseFloat(e.target.value) }))}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Quality (1-10)
              </label>
              <Input
                type="number"
                min="1"
                max="10"
                value={formData.quality || ''}
                onChange={(e) => setFormData(prev => ({ ...prev, quality: parseInt(e.target.value) }))}
                required
              />
            </div>
          </>
        );
      
      case 'water':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Water Intake (ml)
            </label>
            <Input
              type="number"
              value={formData.amount_ml || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, amount_ml: parseInt(e.target.value) }))}
              required
            />
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="w-full max-w-md"
      >
        <Card className="neon-border">
          <CardHeader>
            <CardTitle className="capitalize">Log {type}</CardTitle>
            <CardDescription>Add your {type} data to track progress</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {renderForm()}
              <div className="flex space-x-2 pt-4">
                <Button type="submit" className="flex-1">Save</Button>
                <Button type="button" variant="outline" onClick={onClose} className="flex-1">
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

import { ProtectedRoute } from '@/components/ProtectedRoute';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState<UserStats | null>(null);
  const [dailyReport, setDailyReport] = useState<DailyReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water' | null;
  }>({ isOpen: false, type: null });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [statsResponse, reportResponse] = await Promise.all([
        ApiClient.getUserStats(),
        ApiClient.getDailyReport(),
      ]);
      
      setStats(statsResponse as UserStats);
      setDailyReport((reportResponse as any).report as DailyReport);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogging = (type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water') => {
    setModalState({ isOpen: true, type });
  };

  const handleLogSubmit = async (data: any) => {
    try {
      switch (modalState.type) {
        case 'mood':
          await ApiClient.logMood(data);
          break;
        case 'meal':
          await ApiClient.logMeal(data);
          break;
        case 'exercise':
          await ApiClient.logExercise(data);
          break;
        case 'sleep':
          await ApiClient.logSleep(data);
          break;
        case 'water':
          await ApiClient.logWater(data);
          break;
      }
      
      // Reload dashboard data
      loadDashboardData();
    } catch (error) {
      console.error('Error logging data:', error);
    }
  };

  const xpToNextLevel = stats ? Math.ceil((stats.current_level + 1) * 100) : 100;
  const currentLevelXp = stats ? stats.total_xp % 100 : 0;
  const xpProgress = (currentLevelXp / 100) * 100;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="glass-effect p-8 rounded-lg">
          <div className="animate-pulse text-blue-400">Loading your progress...</div>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-between items-center"
        >
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <User className="w-8 h-8 text-blue-400" />
              <h1 className="text-3xl font-bold text-white">Welcome back, {user?.username}!</h1>
            </div>
          </div>
          
          <Button variant="outline" onClick={logout}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </motion.div>

        {/* Level & XP Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="neon-border">
            <CardContent className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="level-badge text-xl mb-2">
                    Level {stats?.current_level || 1}
                  </div>
                  <div className="text-gray-400">Current Level</div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">XP Progress</span>
                    <span className="text-blue-400">{currentLevelXp}/100</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-4">
                    <div 
                      className="xp-bar h-4 rounded-full transition-all duration-500"
                      style={{ width: `${xpProgress}%` }}
                    />
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-400">
                    {stats?.total_xp || 0}
                  </div>
                  <div className="text-gray-400">Total XP</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Today's Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5" />
                <span>Today's Progress</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="glass-effect p-4 rounded-lg text-center">
                  <Zap className="w-8 h-8 text-yellow-400 mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">{stats?.todays_xp || 0}</div>
                  <div className="text-sm text-gray-400">XP Today</div>
                </div>
                
                <div className="glass-effect p-4 rounded-lg text-center">
                  <Trophy className="w-8 h-8 text-purple-400 mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">
                    {dailyReport?.achievements?.length || 0}
                  </div>
                  <div className="text-sm text-gray-400">Achievements</div>
                </div>
                
                <div className="glass-effect p-4 rounded-lg text-center">
                  <Activity className="w-8 h-8 text-green-400 mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">
                    {dailyReport?.health_score || 0}%
                  </div>
                  <div className="text-sm text-gray-400">Health Score</div>
                </div>
                
                <div className="glass-effect p-4 rounded-lg text-center">
                  <Brain className="w-8 h-8 text-blue-400 mx-auto mb-2" />
                  <div className="text-lg font-bold text-white">
                    {dailyReport?.mood_average?.toFixed(1) || 'N/A'}
                  </div>
                  <div className="text-sm text-gray-400">Avg Mood</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Logging Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calendar className="w-5 h-5" />
                <span>Quick Log</span>
              </CardTitle>
              <CardDescription>
                Track your daily activities to earn XP and level up
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <Button
                  variant="secondary"
                  onClick={() => handleLogging('mood')}
                  className="p-6 h-auto flex-col"
                >
                  <Brain className="w-8 h-8 mb-2" />
                  <span>Log Mood</span>
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => handleLogging('meal')}
                  className="p-6 h-auto flex-col"
                >
                  <Utensils className="w-8 h-8 mb-2" />
                  <span>Log Meal</span>
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => handleLogging('exercise')}
                  className="p-6 h-auto flex-col"
                >
                  <Dumbbell className="w-8 h-8 mb-2" />
                  <span>Log Exercise</span>
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => handleLogging('sleep')}
                  className="p-6 h-auto flex-col"
                >
                  <Moon className="w-8 h-8 mb-2" />
                  <span>Log Sleep</span>
                </Button>
                
                <Button
                  variant="secondary"
                  onClick={() => handleLogging('water')}
                  className="p-6 h-auto flex-col"
                >
                  <Droplets className="w-8 h-8 mb-2" />
                  <span>Log Water</span>
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Code Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Code2 className="w-5 h-5" />
                <span>Code Activity</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <Code2 className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400 mb-4">Code activity tracking coming soon!</p>
                <Button variant="outline">
                  Connect Git Repository
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Logging Modal */}
      <LoggingModal
        isOpen={modalState.isOpen}
        onClose={() => setModalState({ isOpen: false, type: null })}
        type={modalState.type!}
        onSubmit={handleLogSubmit}
      />
      </div>
    </ProtectedRoute>
  );
}
