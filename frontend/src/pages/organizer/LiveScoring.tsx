import { GlassCard } from '../../components/ui/GlassCard'
import { NeonButton } from '../../components/ui/NeonButton'

export default function LiveScoring() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Live Scoring</h1>
        <p className="text-gray-400">Score matches in real-time</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Match 1</h2>
          <div className="space-y-4">
            <div className="p-4 bg-dark-bg-tertiary rounded-lg">
              <p className="text-white font-bold text-2xl mb-1">Team A</p>
              <p className="text-neon-blue text-3xl font-bold">120/5 (6.0)</p>
            </div>
            <div className="p-4 bg-dark-bg-tertiary rounded-lg">
              <p className="text-white font-bold text-2xl mb-1">Team B</p>
              <p className="text-neon-blue text-3xl font-bold">0/0 (0.0)</p>
            </div>
            <NeonButton className="w-full">Add Ball</NeonButton>
          </div>
        </GlassCard>

        <GlassCard>
          <h2 className="text-xl font-bold neon-text mb-4">Ball-by-Ball</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {Array.from({ length: 10 }).map((_, i) => (
              <div key={i} className="p-3 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
                <p className="text-white text-sm">Over {Math.floor(i / 6) + 1}.{i % 6 + 1}</p>
                <p className="text-gray-400 text-xs">Batsman: Player {i + 1}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </div>
    </div>
  )
}

