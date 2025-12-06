import { GlassCard } from '../../components/ui/GlassCard'
import { NeonButton } from '../../components/ui/NeonButton'
import { Calendar } from 'lucide-react'

export default function MatchScheduler() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold neon-text mb-2">Match Scheduler</h1>
          <p className="text-gray-400">Schedule and manage matches</p>
        </div>
        <NeonButton>
          <Calendar size={20} className="mr-2" />
          Generate Schedule
        </NeonButton>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4">Match Calendar</h2>
        <div className="grid grid-cols-7 gap-4">
          {Array.from({ length: 21 }).map((_, i) => (
            <div
              key={i}
              className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20 hover:border-neon-blue transition-all cursor-pointer"
            >
              <p className="text-sm text-gray-400">Match {i + 1}</p>
              <p className="text-white font-medium mt-1">Team A vs Team B</p>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

