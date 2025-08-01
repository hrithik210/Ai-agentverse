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
  Zap, 
  Brain, 
  Code2, 
  Utensils, 
  Dumbbell, 
  Moon, 
  Droplets,
  LogOut,
  TrendingUp,
  Calendar,
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
          <h4 className="text-lg font-semibold text-gradient mb-3 flex items-center">
            <span className="mr-2">⚡</span>
            XP Breakdown
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {sections.xpBreakdown.map((item: any, index: number) => (
              <div
                key={index}
                className="premium-glass p-4 rounded-xl border border-amber-500/20"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-xl">{categoryIcons[item.category] || '⭐'}</span>
                    <span className="text-white font-medium">
                      {item.category.replace('Health_', '')}
                    </span>
                  </div>
                  <span className="text-gradient font-bold text-lg">+{item.xp} XP</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Total XP Today */}
      {sections.totalXP && (
        <div className="text-center p-6 premium-glass rounded-xl border border-amber-500/30">
          <div className="flex items-center justify-center space-x-3">
            <span className="text-3xl">🏆</span>
            <span className="text-2xl font-bold text-gradient">
              Total XP Today: +{sections.totalXP}
            </span>
          </div>
        </div>
      )}

      {/* Activity Summaries */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sections.mood && (
          <div className="premium-glass p-5 rounded-xl border border-amber-500/20">
            <div className="flex items-center space-x-3 mb-3">
              <span className="text-xl">🧠</span>
              <span className="font-semibold text-gradient">Mood</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">{sections.mood}</p>
          </div>
        )}

        {sections.health && (
          <div className="premium-glass p-5 rounded-xl border border-amber-500/20">
            <div className="flex items-center space-x-3 mb-3">
              <span className="text-xl">💪</span>
              <span className="font-semibold text-gradient">Health</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">{sections.health}</p>
          </div>
        )}

        {sections.code && (
          <div className="premium-glass p-5 rounded-xl border border-amber-500/20">
            <div className="flex items-center space-x-3 mb-3">
              <span className="text-xl">⌨️</span>
              <span className="font-semibold text-gradient">Code</span>
            </div>
            <p className="text-gray-300 text-sm leading-relaxed">{sections.code}</p>
          </div>
        )}
      </div>

      {/* Overall Summary */}
      {sections.overall && (
        <div className="premium-glass p-6 rounded-xl border border-amber-500/20">
          <div className="flex items-center space-x-3 mb-4">
            <span className="text-xl">🎯</span>
            <span className="font-semibold text-gradient text-lg">Daily Insight</span>
          </div>
          <p className="text-gray-300 leading-relaxed">{sections.overall}</p>
        </div>
      )}

      {/* Level Progress */}
      {sections.level && sections.totalXPEver && (
        <div className="text-center p-4 premium-glass rounded-xl border border-amber-500/30">
          <div className="flex items-center justify-center space-x-6">
            <div className="flex items-center space-x-2">
              <span className="text-xl">🧬</span>
              <span className="text-gradient font-semibold text-lg">Level {sections.level}</span>
            </div>
            <div className="text-gray-500">•</div>
            <div className="text-gradient font-semibold text-lg">
              {sections.totalXPEver} Total XP
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

// XP Notification Component
const XPNotificationComponent = ({ notifications}: { 
  notifications: XPNotification[], 
  onDismiss: (id: string) => void 
}) => {
  return (
    <div className="fixed top-6 right-6 z-50 space-y-3">
      <AnimatePresence>
        {notifications.map((notification) => (
          <motion.div
            key={notification.id}
            initial={{ opacity: 0, x: 100, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, x: 0, scale: 1, y: 0 }}
            exit={{ opacity: 0, x: 100, scale: 0.9, y: 0 }}
            transition={{
              type: "spring",
              stiffness: 300,
              damping: 30
            }}
            className="bg-gradient-to-r from-amber-400 to-amber-600 text-black px-6 py-4 rounded-2xl shadow-2xl border border-amber-300/50 backdrop-blur-lg"
            style={{
              boxShadow: `
                0 10px 30px -5px rgba(251, 191, 36, 0.3),
                0 5px 15px -3px rgba(251, 191, 36, 0.2)
              `
            }}
          >
            <div className="flex items-center space-x-3">
              <motion.div 
                className="bg-black/20 rounded-full p-2"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring" }}
              >
                <Star className="w-5 h-5 text-amber-100" />
              </motion.div>
              <motion.span 
                className="font-bold text-xl"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                +{notification.amount} XP
              </motion.span>
            </div>
            <motion.div 
              className="text-sm font-medium mt-2 text-amber-900"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              {notification.message}
            </motion.div>
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
            <label className="block text-lg font-medium text-gradient mb-3">
              How are you feeling today?
            </label>
            <Input
              type="text"
              value={formData.mood_text || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, mood_text: e.target.value }))}
              placeholder="I'm feeling great because..."
              className="text-lg py-3"
              required
            />
          </div>
        );
      
      case 'meal':
        return (
          <div>
            <label className="block text-lg font-medium text-gradient mb-3">
              What did you eat?
            </label>
            <Input
              type="text"
              value={formData.meal || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, meal: e.target.value }))}
              placeholder="Grilled chicken with vegetables..."
              className="text-lg py-3"
              required
            />
          </div>
        );
      
      case 'exercise':
        return (
          <div>
            <label className="block text-lg font-medium text-gradient mb-3">
              Exercise Duration (minutes)
            </label>
            <Input
              type="number"
              value={formData.exercise_minutes || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, exercise_minutes: parseInt(e.target.value) }))}
              placeholder="30"
              className="text-lg py-3"
              required
            />
          </div>
        );
      
      case 'sleep':
        return (
          <div>
            <label className="block text-lg font-medium text-gradient mb-3">
              Hours Slept
            </label>
            <Input
              type="number"
              step="0.5"
              value={formData.sleep_hours || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, sleep_hours: parseFloat(e.target.value) }))}
              placeholder="8"
              className="text-lg py-3"
              required
            />
          </div>
        );
      
      case 'water':
        return (
          <div>
            <label className="block text-lg font-medium text-gradient mb-3">
              Water Intake (liters)
            </label>
            <Input
              type="number"
              step="0.1"
              value={formData.water_intake || ''}
              onChange={(e) => setFormData(prev => ({ ...prev, water_intake: parseFloat(e.target.value) }))}
              placeholder="0.5"
              className="text-lg py-3"
              required
            />
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-lg flex items-center justify-center p-6 z-50">
      <motion.div
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        transition={{ type: "spring", duration: 0.5 }}
        className="w-full max-w-lg"
      >
        <Card className="premium-card border-amber-500/30 shadow-2xl">
          <CardHeader className="space-y-2">
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <CardTitle className="capitalize text-2xl font-bold">
                <span className="text-gradient">Log {type}</span>
              </CardTitle>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: -5 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <CardDescription className="text-gray-300 text-lg">
                Track your progress and earn XP instantly!
              </CardDescription>
            </motion.div>
          </CardHeader>
          <CardContent>
            <motion.form 
              onSubmit={handleSubmit} 
              className="space-y-6"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              {renderForm()}
              <motion.div 
                className="flex space-x-4 pt-6"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Button 
                  type="submit" 
                  className="flex-1 premium-button text-black font-semibold text-lg py-3 transition-all duration-300 ease-out hover:scale-105"
                >
                  Save & Earn XP
                </Button>
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={onClose} 
                  className="flex-1 border-amber-500/30 hover:border-amber-400/50 hover:bg-amber-500/10 text-amber-100 py-3 transition-all duration-300"
                >
                  Cancel
                </Button>
              </motion.div>
            </motion.form>
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

  const currentLevelXp = stats ? stats.total_xp % 100 : 0;
  const xpProgress = (currentLevelXp / 100) * 100;

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="premium-glass p-8 rounded-xl border border-amber-500/30">
          <div className="animate-pulse text-gradient text-lg font-semibold">Loading your progress...</div>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen p-4 md:p-6">
        <XPNotificationComponent notifications={xpNotifications} onDismiss={dismissNotification} />
        <div className="max-w-5xl mx-auto space-y-6 md:space-y-8">
          {/* Header - compact */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex flex-col md:flex-row justify-between items-center gap-3 md:gap-6"
          >
            <div className="flex items-center gap-3">
              <div className="p-1.5 premium-glass rounded-lg border border-amber-500/20">
                <User className="w-6 h-6 text-gradient" />
              </div>
              <div>
                <span className="block text-lg md:text-xl text-gray-400">Welcome,</span>
                <span className="block text-xl md:text-2xl font-semibold text-white truncate max-w-xs">{user?.username}</span>
              </div>
            </div>
            <Button
              variant="outline"
              onClick={logout}
              className="border-amber-500/20 hover:border-amber-400/40 hover:bg-amber-500/10 text-amber-100 px-3 py-1.5 text-sm md:text-base flex items-center"
            >
              <LogOut className="w-4 h-4 mr-1" />
              Logout
            </Button>
          </motion.div>

          {/* Level & XP + Today's Stats - compact row */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="premium-card border-amber-500/20 w-full mx-auto">
              <CardContent className="p-3 md:p-4">
                <div className="flex flex-col md:flex-row gap-4 md:gap-8 items-stretch justify-between">
                  {/* Level & XP */}
                  <div className="flex-1 flex flex-col items-center justify-center text-center gap-2 border-b md:border-b-0 md:border-r border-amber-500/10 pb-4 md:pb-0 md:pr-6">
                    <div className="level-badge text-base md:text-lg mb-1 px-3 py-1 font-semibold bg-gray-800/60 rounded-md border border-amber-500/20">
                      Level {stats?.current_level || 1}
                    </div>
                    <div className="text-gray-400 text-xs font-medium">Current Level</div>
                    <div className="flex flex-col items-center mt-1">
                      <div className="text-lg font-bold text-gradient mb-0.5">
                        {stats?.total_xp || 0}
                      </div>
                      <div className="text-gray-400 text-xs font-medium">Total XP</div>
                    </div>
                  </div>
                  {/* XP Progress & Today's XP */}
                  <div className="flex-1 flex flex-col items-center justify-center gap-3">
                    <div className="w-full max-w-xs">
                      <div className="flex justify-between text-xs font-medium mb-1">
                        <span className="text-gray-400">XP Progress</span>
                        <span className="text-gradient font-bold">{currentLevelXp}/100</span>
                      </div>
                      <div className="w-full bg-gray-800/50 rounded-full h-3 border border-amber-500/20 overflow-hidden">
                        <div 
                          className="xp-bar h-3 rounded-full transition-all duration-700 ease-out bg-amber-400/80"
                          style={{ width: `${xpProgress}%` }}
                        />
                      </div>
                    </div>
                    <div className="flex items-center gap-3 mt-2">
                      <div className="p-1 premium-glass rounded-lg border border-amber-500/30 flex items-center justify-center">
                        <Zap className="w-4 h-4 text-gradient" />
                      </div>
                      <div className="flex flex-col items-center">
                        <div className="text-base font-bold text-gradient leading-none">{stats?.todays_xp || 0}</div>
                        <div className="text-gray-400 text-xs font-medium leading-none">XP Today</div>
                      </div>
                      <div className="p-1 premium-glass rounded-full border border-amber-500/30 ml-2 flex items-center justify-center">
                        <TrendingUp className="w-4 h-4 text-amber-400/80" />
                      </div>
                    </div>
                  </div>
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
            <Card className="premium-card border-amber-500/20">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <Calendar className="w-6 h-6 text-gradient" />
                    <span className="text-xl text-gradient">Daily Summary</span>
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
                    className="premium-button text-black font-semibold"
                    disabled={isGeneratingSummary}
                  >
                    <Calendar className="w-4 h-4 mr-2" />
                    {isGeneratingSummary ? 'Generating...' : 'Refresh Summary'}
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
            transition={{ delay: 0.4 }}
          >
            <Card className="premium-card border-amber-500/20">
              <CardHeader>
                <CardTitle className="flex items-center space-x-3">
                  <Plus className="w-6 h-6 text-gradient" />
                  <span className="text-xl text-gradient">Log Activities & Earn XP</span>
                </CardTitle>
                <CardDescription className="text-gray-400 text-lg">Track your daily activities to level up instantly!</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleLogging('mood')}
                    className="group relative flex flex-col items-center space-y-3 p-6 h-28 premium-glass rounded-2xl border border-amber-500/10 hover:border-amber-400/30 transition-all duration-300 overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="relative z-10 p-2 bg-amber-500/10 rounded-xl group-hover:bg-amber-500/20 transition-colors duration-300">
                      <Brain className="w-6 h-6 text-amber-300" />
                    </div>
                    <span className="relative z-10 font-medium text-gray-200 group-hover:text-white transition-colors duration-300">Mood</span>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleLogging('meal')}
                    className="group relative flex flex-col items-center space-y-3 p-6 h-28 premium-glass rounded-2xl border border-emerald-500/10 hover:border-emerald-400/30 transition-all duration-300 overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="relative z-10 p-2 bg-emerald-500/10 rounded-xl group-hover:bg-emerald-500/20 transition-colors duration-300">
                      <Utensils className="w-6 h-6 text-emerald-300" />
                    </div>
                    <span className="relative z-10 font-medium text-gray-200 group-hover:text-white transition-colors duration-300">Meal</span>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleLogging('exercise')}
                    className="group relative flex flex-col items-center space-y-3 p-6 h-28 premium-glass rounded-2xl border border-rose-500/10 hover:border-rose-400/30 transition-all duration-300 overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-rose-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="relative z-10 p-2 bg-rose-500/10 rounded-xl group-hover:bg-rose-500/20 transition-colors duration-300">
                      <Dumbbell className="w-6 h-6 text-rose-300" />
                    </div>
                    <span className="relative z-10 font-medium text-gray-200 group-hover:text-white transition-colors duration-300">Exercise</span>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleLogging('sleep')}
                    className="group relative flex flex-col items-center space-y-3 p-6 h-28 premium-glass rounded-2xl border border-indigo-500/10 hover:border-indigo-400/30 transition-all duration-300 overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="relative z-10 p-2 bg-indigo-500/10 rounded-xl group-hover:bg-indigo-500/20 transition-colors duration-300">
                      <Moon className="w-6 h-6 text-indigo-300" />
                    </div>
                    <span className="relative z-10 font-medium text-gray-200 group-hover:text-white transition-colors duration-300">Sleep</span>
                  </motion.button>
                  
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleLogging('water')}
                    className="group relative flex flex-col items-center space-y-3 p-6 h-28 premium-glass rounded-2xl border border-cyan-500/10 hover:border-cyan-400/30 transition-all duration-300 overflow-hidden"
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                    <div className="relative z-10 p-2 bg-cyan-500/10 rounded-xl group-hover:bg-cyan-500/20 transition-colors duration-300">
                      <Droplets className="w-6 h-6 text-cyan-300" />
                    </div>
                    <span className="relative z-10 font-medium text-gray-200 group-hover:text-white transition-colors duration-300">Water</span>
                  </motion.button>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Code Activity Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="premium-card border-amber-500/20">
              <CardHeader>
                <CardTitle className="flex items-center space-x-3">
                  <Code2 className="w-6 h-6 text-gradient" />
                  <span className="text-xl text-gradient">Coding Activity</span>
                </CardTitle>
                <CardDescription className="text-gray-400 text-lg">Log your coding sessions and earn bonus XP!</CardDescription>
              </CardHeader>
              <CardContent>


                  <h2>
                    <span className="text-lg font-semibold text-gradient">Coming Soon!</span>
                  </h2>
                
                
                {/* <div className="flex space-x-4">
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
                    className="premium-button text-black font-semibold text-lg px-8 py-4"
                  >
                    <Code2 className="w-5 h-5 mr-3" />
                    Log Code Session
                  </Button>
                </div> */}
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
