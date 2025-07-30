# HigherMe Frontend

A modern Next.js frontend application for HigherMe - a solo leveling system that gamifies personal development through mood tracking, health logging, and coding activity monitoring.

## 🌟 Features

- **Solo Leveling System**: Gamified experience with XP, levels, and achievements
- **Mood Tracking**: Monitor your mental state and emotional well-being
- **Health Logging**: Track meals, exercise, sleep, and water intake
- **Code Activity**: Monitor your coding progress and activity
- **Modern UI**: Dark cyberpunk-inspired theme with glass morphism effects
- **Real-time Progress**: Live XP tracking and level progression
- **Responsive Design**: Optimized for desktop and mobile devices

## 🛠 Tech Stack

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI primitives
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Authentication**: JWT-based auth with local storage

## 🚀 Getting Started

### Prerequisites

- Node.js 18.0 or later
- npm or yarn package manager
- HigherMe backend server running on `http://localhost:8000`

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd HigherMe/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   # Create .env.local file
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) in your browser

## 📱 Application Structure

### Pages
- **Landing Page** (`/`): Authentication (login/register) with feature showcase
- **Dashboard** (`/dashboard`): Main application interface with level tracking and logging

### Key Components
- `AuthProvider`: Global authentication state management
- `ProtectedRoute`: Route protection for authenticated users
- `LoggingModal`: Universal modal for all logging activities
- `UI Components`: Reusable components with consistent theming

### Features
- **Level System**: Visual level badges and XP progress bars
- **Quick Logging**: One-click logging for mood, health, and activities  
- **Daily Reports**: Summary of progress and achievements
- **Real-time Updates**: Immediate feedback on actions and progress

## 🎨 Design System

### Colors
- **Primary**: Electric blue (`#3B82F6`) to cyan (`#06B6D4`)
- **Secondary**: Purple (`#8B5CF6`) gradients
- **Background**: Dark gradients (navy to black)
- **Accent**: Neon effects and glass morphism

### Components
- Glass morphism effects with backdrop blur
- Neon border accents on interactive elements
- Smooth animations and transitions
- Consistent spacing and typography

## 🔧 Development

### Available Scripts

```bash
# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Project Structure

```
src/
├── app/                 # Next.js App Router pages
│   ├── dashboard/       # Dashboard page
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Landing page
├── components/          # Reusable components
│   ├── ui/             # Base UI components
│   └── ProtectedRoute.tsx
├── hooks/              # Custom React hooks
│   └── useAuth.tsx     # Authentication hook
├── lib/                # Utility functions
│   ├── api.ts          # API client
│   └── utils.ts        # Helper functions
└── types/              # TypeScript definitions
    └── api.ts          # API type definitions
```

## 🌐 API Integration

The frontend integrates with the HigherMe backend through a REST API:

- **Authentication**: `/auth/login`, `/auth/register`
- **User Stats**: `/stats` (levels, XP, progress)
- **Logging**: `/mood`, `/health/*`, `/code-activity`
- **Reports**: `/daily-report`

## 🎯 Future Enhancements

- [ ] Code activity integration with Git repositories
- [ ] Achievement system with badges
- [ ] Social features and leaderboards  
- [ ] Mobile app with React Native
- [ ] Advanced analytics and insights
- [ ] Integration with fitness trackers
- [ ] Habit tracking system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Next.js team for the excellent framework
- Radix UI for accessible component primitives
- Tailwind CSS for utility-first styling
- Framer Motion for smooth animations
