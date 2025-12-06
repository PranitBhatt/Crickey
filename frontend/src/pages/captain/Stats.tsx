import { GlassCard } from '../../components/ui/GlassCard'
import { BarChart3 } from 'lucide-react'

export default function Stats() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Statistics</h1>
        <p className="text-gray-400">Team and player statistics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Team Stats</h2>
          <div className="space-y-3">
            <div className="flex justify-between p-3 bg-dark-bg-tertiary rounded-lg">
              <span className="text-gray-400">Matches Played</span>
              <span className="text-neon-blue font-bold">3</span>
            </div>
            <div className="flex justify-between p-3 bg-dark-bg-tertiary rounded-lg">
              <span className="text-gray-400">Wins</span>
              <span className="text-green-400 font-bold">2</span>
            </div>
            <div className="flex justify-between p-3 bg-dark-bg-tertiary rounded-lg">
              <span className="text-gray-400">Losses</span>
              <span className="text-red-400 font-bold">1</span>
            </div>
          </div>
        </GlassCard>

        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Top Performers</h2>
          <div className="space-y-3">
            {['Player 1', 'Player 2', 'Player 3'].map((player, i) => (
              <div key={i} className="p-3 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
                <p className="text-white font-medium">{player}</p>
                <p className="text-gray-400 text-sm">120 runs, 5 wickets</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

