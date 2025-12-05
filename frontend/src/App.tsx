import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { onAuthStateChange } from './services/authService';
import { useAuthStore } from './store/authStore';
import { PrivateRoute } from './components/PrivateRoute';
import { Login } from './pages/Login';
import { OrganizerDashboard } from './pages/Organizer/Dashboard';
import { CreateTournament } from './pages/Organizer/CreateTournament';
import { TournamentDetail } from './pages/Organizer/TournamentDetail';
import { MatchScoring } from './pages/Organizer/MatchScoring';
import { CaptainDashboard } from './pages/Captain/Dashboard';

function App() {
  const { setUser, setLoading, loadProfile } = useAuthStore();

  useEffect(() => {
    const unsubscribe = onAuthStateChange(async (user) => {
      setUser(user);
      if (user) {
        await loadProfile(user.uid);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [setUser, setLoading, loadProfile]);

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route
            path="/organizer"
            element={
              <PrivateRoute requiredRole="organizer">
                <OrganizerDashboard />
              </PrivateRoute>
            }
          />
          <Route
            path="/organizer/tournaments/create"
            element={
              <PrivateRoute requiredRole="organizer">
                <CreateTournament />
              </PrivateRoute>
            }
          />
          <Route
            path="/organizer/tournaments/:id"
            element={
              <PrivateRoute requiredRole="organizer">
                <TournamentDetail />
              </PrivateRoute>
            }
          />
          <Route
            path="/organizer/matches/:id/score"
            element={
              <PrivateRoute requiredRole="organizer">
                <MatchScoring />
              </PrivateRoute>
            }
          />
          <Route
            path="/captain"
            element={
              <PrivateRoute requiredRole="captain">
                <CaptainDashboard />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </>
  );
}

export default App;

