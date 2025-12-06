import { GlassCard } from '../../components/ui/GlassCard'
import { NeonButton } from '../../components/ui/NeonButton'
import { Plus } from 'lucide-react'

export default function TeamsManagement() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold neon-text mb-2">Teams Management</h1>
          <p className="text-gray-400">Manage tournament teams</p>
        </div>
        <NeonButton>
          <Plus size={20} className="mr-2" />
          Add Team
        </NeonButton>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <GlassCard key={i} className="p-6">
            <h3 className="text-xl font-bold text-white mb-2">Team {String.fromCharCode(64 + i)}</h3>
            <p className="text-gray-400 mb-4">Group {i % 2 === 0 ? 'A' : 'B'}</p>
            <div className="flex gap-2">
              <NeonButton variant="secondary" className="flex-1">Edit</NeonButton>
              <NeonButton variant="danger" className="flex-1">Delete</NeonButton>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  )
}

