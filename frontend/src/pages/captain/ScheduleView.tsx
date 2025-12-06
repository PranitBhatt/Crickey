import { GlassCard } from '../../components/ui/GlassCard'

export default function ScheduleView() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Match Schedule</h1>
        <p className="text-gray-400">View upcoming matches</p>
      </div>

      <GlassCard>
        <h2 className="text-xl font-bold neon-text mb-4">Upcoming Matches</h2>
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="p-4 bg-dark-bg-tertiary rounded-lg border border-neon-blue/20">
              <div className="flex justify-between items-center">
                <div>
                  <p className="text-white font-medium">Match {i + 1}</p>
                  <p className="text-gray-400 text-sm">vs Team {String.fromCharCode(65 + i)}</p>
                </div>
                <div className="text-right">
                  <p className="text-neon-blue">Tomorrow</p>
                  <p className="text-gray-400 text-sm">10:00 AM</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  )
}

