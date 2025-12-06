/**
 * Points table service.
 */
import apiClient from './apiClient'

export interface PointsTableEntry {
  team_id: number
  team_name: string
  group: string
  played: number
  won: number
  lost: number
  tied: number
  points: number
  net_run_rate: number
  runs_for: number
  runs_against: number
  overs_for: number
  overs_against: number
}

export interface PointsTable {
  id: number
  tournament_id: number
  group: string
  entries: PointsTableEntry[]
  last_updated: string
}

export const pointsService = {
  async calculate(tournamentId: number, group: string): Promise<PointsTable> {
    const response = await apiClient.post<PointsTable>(
      `/points-table/calculate/${tournamentId}/${group}`
    )
    return response.data
  },

  async get(tournamentId: number, group: string): Promise<PointsTable> {
    const response = await apiClient.get<PointsTable>(`/points-table/${tournamentId}/${group}`)
    return response.data
  },

  async getAll(tournamentId: number): Promise<PointsTable[]> {
    const response = await apiClient.get<PointsTable[]>(`/points-table/${tournamentId}`)
    return response.data
  },
}

