'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
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
  Activity,
  Plus,
  Star
} from 'lucide-react';
import { ProtectedRoute } from '@/components/ProtectedRoute';

interface XPNotification {
  id: string;
  amount: number;
  message: string;
  type: string;
}

interface LoggingModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water';
  onSubmit: (data: any) => void;
}

// Daily Report Parser Component
const DailyReportComponent = ({ report }: { report: string }) => {
  if (!report) return <p className="text-gray-400">No summary available for today.</p>;

  const parseReport = (reportText: string) => {
    const lines = reportText.split('\n').filter(line => line.trim());
    const sections: any = {};
    let currentSection = '';

    lines.forEach(line => {
      if (line.includes('**Daily Report**')) {
        currentSection = 'title';
        sections.title = line.replace(/[🌅*]/g, '').trim();
      } else if (line.includes('**XP Breakdown:**')) {
        currentSection = 'xpBreakdown';
        sections.xpBreakdown = [];
      } else if (line.includes('**Total XP Today:**')) {
        sections.totalXP = line.match(/\+(\d+)/)?.[1] || '0';
      } else if (line.includes('**Mood:**')) {
        sections.mood = line.replace(/[🧠*]/g, '').replace('Mood:', '').trim();
      } else if (line.includes('**Health:**')) {
        sections.health = line.replace(/[💪*]/g, '').replace('Health:', '').trim();
      } else if (line.includes('**Code:**')) {
        sections.code = line.replace(/[⌨️*]/g, '').replace('Code:', '').trim();
      } else if (line.includes('**Overall:**')) {
        sections.overall = line.replace(/[🎯*]/g, '').replace('Overall:', '').trim();
      } else if (line.includes('Current Level:')) {
        const match = line.match(/Level: (\d+).*Total XP: (\d+)/);
        if (match) {
          sections.level = match[1];
          sections.totalXPEver = match[2];
        }
      } else if (currentSection === 'xpBreakdown' && line.includes('- ')) {
        const xpMatch = line.match(/- ([^:]+): \+(\d+) XP/);
        if (xpMatch) {
          sections.xpBreakdown.push({
            category: xpMatch[1],
            xp: xpMatch[2]
          });
        }
      }
    });

    return sections;
  };

  const sections = parseReport(report);
  const categoryIcons: Record<string, string> = {
    'Mood': '🧠',
    'Code': '💻',
    'Health_exercise': '💪',
    'Health_sleep': '😴',
    'Health_meal': '🍽️',
    'Health_water': '💧'
  };

  return (
    <div className="space-y-4">
      {/* XP Breakdown Section */}
      {sections.xpBreakdown && sections.xpBreakdown.length > 0 && (
        <div>
          <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
            <span className="mr-2">🔢</span>
            XP Breakdown
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {sections.xpBreakdown.map((item: any, index: number) => (
              <div
                key={index}
                className="glass-effect p-3 rounded-lg border border-gray-700"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{categoryIcons[item.category] || '⭐'}</span>
                    <span className="text-white font-medium">
                      {item.category.replace('Health_', '')}
                    </span>
                  </div>
                  <span className="text-blue-400 font-bold">+{item.xp} XP</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Total XP Today */}
      {sections.totalXP && (
        <div className="text-center p-4 glass-effect rounded-lg border border-gray-700">
          <div className="flex items-center justify-center space-x-2">
            <span className="text-2xl">🏆</span>
            <span className="text-xl font-bold text-blue-400">
              Total XP Today: +{sections.totalXP}
            </span>
          </div>
        </div>
      )}

      {/* Activity Summaries */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sections.mood && (
          <div className="glass-effect p-4 rounded-lg border border-gray-700">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">🧠</span>
              <span className="font-semibold text-blue-400">Mood</span>
            </div>
            <p className="text-gray-300 text-sm">{sections.mood}</p>
          </div>
        )}

        {sections.health && (
          <div className="glass-effect p-4 rounded-lg border border-gray-700">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">💪</span>
              <span className="font-semibold text-blue-400">Health</span>
            </div>
            <p className="text-gray-300 text-sm">{sections.health}</p>
          </div>
        )}

        {sections.code && (
          <div className="glass-effect p-4 rounded-lg border border-gray-700">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg">⌨️</span>
              <span className="font-semibold text-blue-400">Code</span>
            </div>
            <p className="text-gray-300 text-sm">{sections.code}</p>
          </div>
        )}
      </div>

      {/* Overall Summary */}
      {sections.overall && (
        <div className="glass-effect p-4 rounded-lg border border-gray-700">
          <div className="flex items-center space-x-2 mb-3">
            <span className="text-lg">🎯</span>
            <span className="font-semibold text-blue-400">Daily Insight</span>
          </div>
          <p className="text-gray-300 leading-relaxed">{sections.overall}</p>
        </div>
      )}

      {/* Level Progress */}
      {sections.level && sections.totalXPEver && (
        <div className="text-center p-3 glass-effect rounded-lg border border-gray-700">
          <div className="flex items-center justify-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-lg">🧬</span>
              <span className="text-blue-400 font-semibold">Level {sections.level}</span>
            </div>
            <div className="text-gray-400">•</div>
            <div className="text-blue-400 font-semibold">
              {sections.totalXPEver} Total XP
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// XP Notification Component
const XPNotificationComponent = ({ notifications, onDismiss }: { 
  notifications: XPNotification[], 
  onDismiss: (id: string) => void 
}) => {
  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, x: 100, scale: 0.8 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, x: 100, scale: 0.8 }}
            className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-6 py-3 rounded-lg shadow-lg border border-yellow-300"
          >
            <div className="flex items-center space-x-2">
              <Star className="w-5 h-5" />
              <span className="font-bold">+{notification.amount} XP</span>
            </div>
            <div className="text-sm opacity-90">{notification.message}</div>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
};

// Logging Modal Component
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
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              How are you feeling today?
            </label>
            <Input
              type="text"
              value={formData.mood_text || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, mood_text: e.target.value }))}
              placeholder="I'm feeling great because..."
              required
            />
          </div>
        );
      
      case 'meal':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              What did you eat?
            </label>
            <Input
              type="text"
              value={formData.meal || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, meal: e.target.value }))}
              placeholder="Grilled chicken with vegetables..."
              required
            />
          </div>
        );
      
      case 'exercise':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Exercise Duration (minutes)
            </label>
            <Input
              type="number"
              value={formData.exercise_minutes || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, exercise_minutes: parseInt(e.target.value) }))}
              placeholder="30"
              required
            />
          </div>
        );
      
      case 'sleep':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Hours Slept
            </label>
            <Input
              type="number"
              step="0.5"
              value={formData.sleep_hours || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, sleep_hours: parseFloat(e.target.value) }))}
              placeholder="8"
              required
            />
          </div>
        );
      
      case 'water':
        return (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Water Intake (liters)
            </label>
            <Input
              type="number"
              step="0.1"
              value={formData.water_intake || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, water_intake: parseFloat(e.target.value) }))}
              placeholder="0.5"
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
            <CardDescription>Add your {type} data and earn XP instantly!</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {renderForm()}
              <div className="flex space-x-2 pt-4">
                <Button type="submit" className="flex-1">Save & Earn XP</Button>
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

// Main Dashboard Component
export default function Dashboard() {
  const { user, logout } = useAuth();
  const [stats, setStats] = useState<UserStats | null>(null);
  const [dailyReport, setDailyReport] = useState<DailyReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [modalState, setModalState] = useState<{
    isOpen: boolean;
    type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water' | null;
  }>({ isOpen: false, type: null });
  const [xpNotifications, setXpNotifications] = useState<XPNotification[]>([]);

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
      setDailyReport(reportResponse as DailyReport);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const showXPNotification = (amount: number, message: string, type: string) => {
    const notification: XPNotification = {
      id: Date.now().toString(),
      amount,
      message,
      type
    };
    
    setXpNotifications(prev => [...prev, notification]);
    
    // Auto-dismiss after 4 seconds
    setTimeout(() => {
      setXpNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 4000);
  };

  const handleLogging = (type: 'mood' | 'meal' | 'exercise' | 'sleep' | 'water') => {
    setModalState({ isOpen: true, type });
  };

  const handleLogSubmit = async (data: any) => {
    try {
      const previousXP = stats?.total_xp || 0;
      
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
      
      // Get fresh stats directly from API to calculate actual XP gained
      const freshStatsResponse = await ApiClient.getUserStats();
      const newXP = (freshStatsResponse as UserStats).total_xp;
      const xpGained = newXP - previousXP;
      
      // Update dashboard data with fresh stats
      await loadDashboardData();
      
      // Show notification with actual XP gained
      const typeEmojis = {
        mood: '🧠',
        meal: '🍽️',
        exercise: '💪',
        sleep: '😴',
        water: '💧'
      };
      const emoji = typeEmojis[modalState.type!] || '⭐';
      
      if (xpGained > 0) {
        showXPNotification(xpGained, `${emoji} Great ${modalState.type} log!`, modalState.type!);
      } else {
        // Fallback - should rarely happen now
        showXPNotification(10, `${emoji} ${modalState.type} logged successfully!`, modalState.type!);
      }
      
    } catch (error) {
      console.error('Error logging data:', error);
    }
  };

  const dismissNotification = (id: string) => {
    setXpNotifications(prev => prev.filter(n => n.id !== id));
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
        <XPNotificationComponent notifications={xpNotifications} onDismiss={dismissNotification} />
        
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

          {/* Today's Stats - Compact */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Zap className="w-6 h-6 text-yellow-400" />
                    <div>
                      <div className="text-lg font-bold text-white">{stats?.todays_xp || 0}</div>
                      <div className="text-sm text-gray-400">XP Today</div>
                    </div>
                  </div>
                  <TrendingUp className="w-5 h-5 text-gray-400" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Daily Report - always show summary */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Calendar className="w-5 h-5" />
                    <span>Daily Summary</span>
                  </div>
                  <Button
                    onClick={async () => {
                      try {
                        setIsGeneratingSummary(true);
                        await loadDashboardData();
                        showXPNotification(0, '📊 Daily summary refreshed!', 'summary');
                      } catch (error) {
                        console.error('Error refreshing daily summary:', error);
                      } finally {
                        setIsGeneratingSummary(false);
                      }
                    }}
                    variant="outline"
                    size="sm"
                    className="text-sm"
                    disabled={isGeneratingSummary}
                  >
                    <Calendar className="w-4 h-4 mr-1" />
                    {isGeneratingSummary ? 'Generating...' : 'Generate Summary'}
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <DailyReportComponent report={dailyReport?.report || ''} />
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
                  <Plus className="w-5 h-5" />
                  <span>Log Activities & Earn XP</span>
                </CardTitle>
                <CardDescription>Track your daily activities to level up instantly!</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <Button
                    onClick={() => handleLogging('mood')}
                    className="flex flex-col items-center space-y-2 h-20 bg-gradient-to-br from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
                  >
                    <Brain className="w-6 h-6" />
                    <span>Mood</span>
                  </Button>
                  
                  <Button
                    onClick={() => handleLogging('meal')}
                    className="flex flex-col items-center space-y-2 h-20 bg-gradient-to-br from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                  >
                    <Utensils className="w-6 h-6" />
                    <span>Meal</span>
                  </Button>
                  
                  <Button
                    onClick={() => handleLogging('exercise')}
                    className="flex flex-col items-center space-y-2 h-20 bg-gradient-to-br from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700"
                  >
                    <Dumbbell className="w-6 h-6" />
                    <span>Exercise</span>
                  </Button>
                  
                  <Button
                    onClick={() => handleLogging('sleep')}
                    className="flex flex-col items-center space-y-2 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700"
                  >
                    <Moon className="w-6 h-6" />
                    <span>Sleep</span>
                  </Button>
                  
                  <Button
                    onClick={() => handleLogging('water')}
                    className="flex flex-col items-center space-y-2 h-20 bg-gradient-to-br from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700"
                  >
                    <Droplets className="w-6 h-6" />
                    <span>Water</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Code Activity Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Code2 className="w-5 h-5" />
                  <span>Coding Activity</span>
                </CardTitle>
                <CardDescription>Log your coding sessions and earn bonus XP!</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex space-x-4">
                  <Button
                    onClick={async () => {
                      try {
                        const previousXP = stats?.total_xp || 0;
                        await ApiClient.createCodeActivity();
                        
                        // Get fresh stats directly from API to calculate actual XP gained
                        const freshStatsResponse = await ApiClient.getUserStats();
                        const newXP = (freshStatsResponse as UserStats).total_xp;
                        const xpGained = newXP - previousXP;
                        
                        // Update dashboard data with fresh stats
                        await loadDashboardData();
                        
                        // Show notification with actual XP gained
                        if (xpGained > 0) {
                          showXPNotification(xpGained, '💻 Code session logged!', 'code');
                        } else {
                          // Fallback - should rarely happen now
                          showXPNotification(25, '💻 Code session logged!', 'code');
                        }
                      } catch (error) {
                        console.error('Error creating code activity:', error);
                      }
                    }}
                    className="bg-gradient-to-br from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700"
                  >
                    <Code2 className="w-4 h-4 mr-2" />
                    Log Code Session
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

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
