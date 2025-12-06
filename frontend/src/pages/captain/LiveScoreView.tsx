import { GlassCard } from '../../components/ui/GlassCard'
import { Target } from 'lucide-react'

export default function LiveScoreView() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Live Scores</h1>
        <p className="text-gray-400">Real-time match updates</p>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4 flex items-center gap-2">
          <Target className="text-green-400" size={24} />
          Live Match
        </h2>
        <div className="space-y-4">
          <div className="p-6 bg-dark-bg-tertiary rounded-lg border border-green-500/30">
            <p className="text-white font-bold text-2xl mb-2">Team A</p>
            <p className="text-green-400 text-4xl font-bold">120/5 (6.0)</p>
          </div>
          <div className="p-6 bg-dark-bg-tertiary rounded-lg border border-neon-blue/30">
            <p className="text-white font-bold text-2xl mb-2">Team B</p>
            <p className="text-neon-blue text-4xl font-bold">0/0 (0.0)</p>
          </div>
        </div>
      </GlassCard>
    </div>
  )
}

