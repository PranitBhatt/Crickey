import { GlassCard } from '../../components/ui/GlassCard'
import { Users } from 'lucide-react'

export default function TeamInfo() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Team Information</h1>
        <p className="text-gray-400">View your team details</p>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4">Players</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {Array.from({ length: 8 }).map((_, i) => (
            <div key={i} className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
              <p className="text-white font-medium">Player {i + 1}</p>
              <p className="text-gray-400 text-sm">Batsman</p>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

