import { GlassCard } from '../../components/ui/GlassCard'
import { Trophy } from 'lucide-react'

export default function PointsTable() {
  const standings = [
    { team: 'Team A', played: 3, won: 2, lost: 1, points: 4, nrr: 0.5 },
    { team: 'Team B', played: 3, won: 2, lost: 1, points: 4, nrr: 0.3 },
    { team: 'Team C', played: 3, won: 1, lost: 2, points: 2, nrr: -0.2 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold neon-text mb-2">Points Table</h1>
        <p className="text-gray-400">Tournament standings</p>
      </div>

      <GlassCard>
        <div className="flex items-center gap-3 mb-6">
          <Trophy className="text-neon-blue" size={24} />
          <h2 className="text-xl font-bold neon-text">Group A</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-neon-blue/30">
                <th className="text-left p-3 text-neon-blue">Team</th>
                <th className="text-center p-3 text-neon-blue">Played</th>
                <th className="text-center p-3 text-neon-blue">Won</th>
                <th className="text-center p-3 text-neon-blue">Lost</th>
                <th className="text-center p-3 text-neon-blue">Points</th>
                <th className="text-center p-3 text-neon-blue">NRR</th>
              </tr>
            </thead>
            <tbody>
              {standings.map((team, i) => (
                <tr key={i} className="border-b border-neon-blue/10">
                  <td className="p-3 text-white font-medium">{team.team}</td>
                  <td className="p-3 text-center text-gray-400">{team.played}</td>
                  <td className="p-3 text-center text-green-400">{team.won}</td>
                  <td className="p-3 text-center text-red-400">{team.lost}</td>
                  <td className="p-3 text-center text-neon-blue font-bold">{team.points}</td>
                  <td className="p-3 text-center text-gray-400">{team.nrr.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </GlassCard>
    </div>
  )
}

