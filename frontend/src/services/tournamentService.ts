/**
 * Tournament service.
 */
import apiClient from './apiClient'

export interface Tournament {
  id: number
  name: string
  start_date: string
  end_date: string
  location: string
  overs_group: number
  overs_knockout: number
  groups: string[]
  status: 'upcoming' | 'ongoing' | 'completed'
  created_by: number
}

export interface TournamentCreate {
  name: string
  start_date: string
  end_date: string
  location: string
  overs_group: number
  overs_knockout: number
  groups: string[]
}

export const tournamentService = {
  async getAll(): Promise<Tournament[]> {
    const response = await apiClient.get<Tournament[]>('/tournaments')
    return response.data
  },

  async getById(id: number): Promise<Tournament> {
    const response = await apiClient.get<Tournament>(`/tournaments/${id}`)
    return response.data
  },

  async create(data: TournamentCreate): Promise<Tournament> {
    const response = await apiClient.post<Tournament>('/tournaments', data)
    return response.data
  },

  async update(id: number, data: Partial<TournamentCreate>): Promise<Tournament> {
    const response = await apiClient.put<Tournament>(`/tournaments/${id}`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(`/tournaments/${id}`)
  },
}
