/**
 * Authentication service.
 */
import apiClient from './apiClient'
import { useAuthStore } from '../store/authStore'

export interface LoginCredentials {
  username: string // email
  password: string
}

export interface RegisterData {
  email: string
  password: string
  name: string
  role: 'organizer' | 'captain'
  phone?: string
}

export interface User {
  id: number
  email: string
  name: string
  role: 'organizer' | 'captain'
  phone?: string
  team_id?: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const response = await apiClient.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    
    useAuthStore.getState().setAuth(response.data.user, response.data.access_token)
    return response.data
  },

  async register(data: RegisterData): Promise<User> {
    const response = await apiClient.post<User>('/auth/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },

  logout() {
    useAuthStore.getState().logout()
  },
}
