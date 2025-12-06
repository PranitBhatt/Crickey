import { GlassCard } from '../../components/ui/GlassCard'
import { Trophy, Users, Calendar, Target } from 'lucide-react'

export default function OrganizerDashboard() {
  const stats = [
    { label: 'Active Tournaments', value: '1', icon: Trophy, color: 'text-neon-blue' },
    { label: 'Total Teams', value: '12', icon: Users, color: 'text-neon-blue-light' },
    { label: 'Matches Today', value: '6', icon: Calendar, color: 'text-neon-blue' },
    { label: 'Live Matches', value: '2', icon: Target, color: 'text-green-400' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Dashboard</h1>
        <p className="text-gray-400">Welcome back, Organizer</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <GlassCard key={stat.label} className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm mb-1">{stat.label}</p>
                  <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
                </div>
                <Icon size={40} className={stat.color} />
              </div>
            </GlassCard>
          )
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Recent Matches</h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-3 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
                <p className="text-white font-medium">Match {i}</p>
                <p className="text-gray-400 text-sm">Team A vs Team B</p>
              </div>
            ))}
          </div>
        </GlassCard>

        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <button className="w-full p-3 bg-neon-blue/20 border border-neon-blue rounded-lg text-neon-blue hover:bg-neon-blue/30 transition-all">
              Create Tournament
            </button>
            <button className="w-full p-3 bg-neon-blue/20 border border-neon-blue rounded-lg text-neon-blue hover:bg-neon-blue/30 transition-all">
              Add Team
            </button>
            <button className="w-full p-3 bg-neon-blue/20 border border-neon-blue rounded-lg text-neon-blue hover:bg-neon-blue/30 transition-all">
              Generate Schedule
            </button>
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

