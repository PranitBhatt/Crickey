import { GlassCard } from '../../components/ui/GlassCard'

export default function Scorecards() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Scorecards</h1>
        <p className="text-gray-400">View completed match scorecards</p>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4">Recent Matches</h2>
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
              <p className="text-white font-medium mb-2">Match {i + 1}</p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-400 text-sm">Team A</p>
                  <p className="text-neon-blue">120/5 (6.0)</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Team B</p>
                  <p className="text-neon-blue">115/7 (6.0)</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

