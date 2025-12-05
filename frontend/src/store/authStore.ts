import { create } from 'zustand';
import { User } from 'firebase/auth';
import { UserProfile, getUserProfile } from '../services/authService';

interface AuthState {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  setUser: (user: User | null) => void;
  setProfile: (profile: UserProfile | null) => void;
  setLoading: (loading: boolean) => void;
  loadProfile: (uid: string) => Promise<void>;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  profile: null,
  loading: true,
  setUser: (user) => set({ user }),
  setProfile: (profile) => set({ profile }),
  setLoading: (loading) => set({ loading }),
  loadProfile: async (uid: string) => {
    const profile = await getUserProfile(uid);
    set({ profile });
  },
  clearAuth: () => set({ user: null, profile: null }),
}));

