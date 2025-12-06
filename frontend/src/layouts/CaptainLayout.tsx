import { Outlet, Link, useLocation } from 'react-router-dom'
import { authService } from '../services/authService'
import { useAuthStore } from '../store/authStore'
import {
  LayoutDashboard,
  Users,
  Calendar,
  Target,
  BarChart3,
  LogOut,
  Menu,
  X,
} from 'lucide-react'
import { useState } from 'react'

export default function CaptainLayout() {
  const location = useLocation()
  const { user } = useAuthStore()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/team', icon: Users, label: 'Team Info' },
    { path: '/schedule', icon: Calendar, label: 'Schedule' },
    { path: '/live', icon: Target, label: 'Live Scores' },
    { path: '/scorecards', icon: Target, label: 'Scorecards' },
    { path: '/stats', icon: BarChart3, label: 'Stats' },
  ]

  const handleLogout = () => {
    authService.logout()
  }

  return (
    <div className="min-h-screen bg-black flex">
      {/* Sidebar */}
      <aside
        className={`
          ${sidebarOpen ? 'w-64' : 'w-20'}
          bg-dark-bg-secondary border-r border-neon-blue/30
          transition-all duration-300 flex flex-col
        `}
      >
        <div className="p-4 border-b border-neon-blue/30 flex items-center justify-between">
          <h1 className={`font-bold neon-text ${sidebarOpen ? 'text-xl' : 'text-sm'}`}>
            {sidebarOpen ? 'Captain' : 'C'}
          </h1>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-neon-blue/20 rounded-lg transition-colors"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`
                  flex items-center gap-3 p-3 rounded-lg transition-all
                  ${isActive
                    ? 'bg-neon-blue/20 border border-neon-blue shadow-neon-sm'
                    : 'hover:bg-neon-blue/10 border border-transparent'
                  }
                `}
              >
                <Icon size={20} className={isActive ? 'text-neon-blue' : 'text-gray-400'} />
                {sidebarOpen && (
                  <span className={isActive ? 'text-neon-blue font-medium' : 'text-gray-400'}>
                    {item.label}
                  </span>
                )}
              </Link>
            )
          })}
        </nav>

        <div className="p-4 border-t border-neon-blue/30">
          <div className="mb-4 p-3 glass rounded-lg">
            {sidebarOpen && (
              <div>
                <p className="text-sm text-gray-400">Logged in as</p>
                <p className="text-neon-blue font-medium">{user?.name}</p>
              </div>
            )}
          </div>
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 p-3 rounded-lg hover:bg-red-500/20 border border-transparent hover:border-red-500 transition-all text-red-400"
          >
            <LogOut size={20} />
            {sidebarOpen && <span>Logout</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

