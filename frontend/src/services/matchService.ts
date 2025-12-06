/**
 * Match service.
 */
import apiClient from './apiClient'

export interface Match {
  id: number
  tournament_id: number
  group?: string
  match_number: number
  team1_id: number
  team2_id: number
  date_time: string
  venue: string
  overs: number
  status: 'scheduled' | 'live' | 'completed'
  winner_team_id?: number
  scores?: Record<string, { runs: number; wickets: number; overs: number }>
}

export interface Ball {
  id: number
  match_id: number
  over_number: number
  ball_number: number
  batsman: string
  bowler: string
  runs: number
  is_wicket: boolean
  extras: number
  timestamp: string
}

export interface ScoreUpdate {
  team_id: number
  runs: number
  wickets: number
  overs: number
}

export interface BallCreate {
  over_number: number
  ball_number: number
  batsman: string
  bowler: string
  runs: number
  is_wicket: boolean
  extras: number
}

export const matchService = {
  async getByTournament(tournamentId: number): Promise<Match[]> {
    const response = await apiClient.get<Match[]>(`/matches/tournament/${tournamentId}`)
    return response.data
  },

  async getById(id: number): Promise<Match> {
    const response = await apiClient.get<Match>(`/matches/${id}`)
    return response.data
  },

  async create(data: Partial<Match>): Promise<Match> {
    const response = await apiClient.post<Match>('/matches', data)
    return response.data
  },

  async update(id: number, data: Partial<Match>): Promise<Match> {
    const response = await apiClient.put<Match>(`/matches/${id}`, data)
    return response.data
  },

  async updateScore(id: number, score: ScoreUpdate): Promise<Match> {
    const response = await apiClient.post<Match>(`/matches/${id}/score`, score)
    return response.data
  },

  async addBall(id: number, ball: BallCreate): Promise<Ball> {
    const response = await apiClient.post<Ball>(`/matches/${id}/ball`, ball)
    return response.data
  },

  async getBalls(id: number): Promise<Ball[]> {
    const response = await apiClient.get<Ball[]>(`/matches/${id}/balls`)
    return response.data
  },
}
