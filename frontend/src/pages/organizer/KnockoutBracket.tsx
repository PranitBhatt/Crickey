import { GlassCard } from '../../components/ui/GlassCard'
import { Trophy } from 'lucide-react'

export default function KnockoutBracket() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Knockout Bracket</h1>
        <p className="text-gray-400">Semi-finals and Final</p>
      </div>

      <GlassCard>
        <div className="flex items-center justify-center gap-8">
          <div className="text-center">
            <h3 className="text-lg font-bold neon-text mb-4">Semi-Final 1</h3>
            <div className="space-y-2">
              <div className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/30">
                <p className="text-white">Team A1</p>
              </div>
              <div className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/30">
                <p className="text-white">Team B2</p>
              </div>
            </div>
          </div>

          <Trophy className="text-neon-blue" size={40} />

          <div className="text-center">
            <h3 className="text-lg font-bold neon-text mb-4">Semi-Final 2</h3>
            <div className="space-y-2">
              <div className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/30">
                <p className="text-white">Team B1</p>
              </div>
              <div className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/30">
                <p className="text-white">Team A2</p>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </div>
  )
}

