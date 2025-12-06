import { GlassCard } from '../../components/ui/GlassCard'
import { Calendar, Target, Trophy } from 'lucide-react'

export default function CaptainDashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Captain Dashboard</h1>
        <p className="text-gray-400">Welcome back, Captain</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <GlassCard className="p-6">
          <div className="flex items-center gap-4">
            <Calendar size={40} className="text-neon-blue" />
            <div>
              <p className="text-gray-400 text-sm">Next Match</p>
              <p className="text-xl font-bold text-white">Tomorrow, 10:00 AM</p>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <div className="flex items-center gap-4">
            <Target size={40} className="text-green-400" />
            <div>
              <p className="text-gray-400 text-sm">Live Matches</p>
              <p className="text-xl font-bold text-white">2 matches</p>
            </div>
          </div>
        </GlassCard>

        <GlassCard className="p-6">
          <div className="flex items-center gap-4">
            <Trophy size={40} className="text-yellow-400" />
            <div>
              <p className="text-gray-400 text-sm">Team Position</p>
              <p className="text-xl font-bold text-white">Group A - 2nd</p>
            </div>
          </div>
        </GlassCard>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4">Upcoming Matches</h2>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-white font-medium">Match {i}</p>
                  <p className="text-gray-400 text-sm">vs Team {String.fromCharCode(65 + i)}</p>
                </div>
                <p className="text-neon-blue">10:00 AM</p>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

