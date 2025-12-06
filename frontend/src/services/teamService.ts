/**
 * Team service.
 */
import apiClient from './apiClient'

export interface Player {
  id: number
  team_id: number
  name: string
  role: string
  is_substitute: boolean
}

export interface Team {
  id: number
  tournament_id: number
  name: string
  group: 'A' | 'B'
  captain_name: string
  captain_uid: number
  logo_url?: string
  players: Player[]
}

export interface TeamCreate {
  tournament_id: number
  name: string
  group: 'A' | 'B'
  captain_name: string
  captain_uid: number
  logo_url?: string
  players: Array<{
    name: string
    role: string
    is_substitute: boolean
  }>
}

export const teamService = {
  async getByTournament(tournamentId: number): Promise<Team[]> {
    const response = await apiClient.get<Team[]>(`/teams/tournament/${tournamentId}`)
    return response.data
  },

  async getById(id: number): Promise<Team> {
    const response = await apiClient.get<Team>(`/teams/${id}`)
    return response.data
  },

  async create(data: TeamCreate): Promise<Team> {
    const response = await apiClient.post<Team>('/teams', data)
    return response.data
  },

  async update(id: number, data: Partial<TeamCreate>): Promise<Team> {
    const response = await apiClient.put<Team>(`/teams/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(`/teams/${id}`)
  },
}
