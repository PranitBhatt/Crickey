import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import Login from './pages/Login'
import OrganizerLayout from './layouts/OrganizerLayout'
import CaptainLayout from './layouts/CaptainLayout'
import OrganizerDashboard from './pages/organizer/Dashboard'
import TeamsManagement from './pages/organizer/TeamsManagement'
import MatchScheduler from './pages/organizer/MatchScheduler'
import LiveScoring from './pages/organizer/LiveScoring'
import PointsTable from './pages/organizer/PointsTable'
import KnockoutBracket from './pages/organizer/KnockoutBracket'
import CaptainDashboard from './pages/captain/Dashboard'
import TeamInfo from './pages/captain/TeamInfo'
import ScheduleView from './pages/captain/ScheduleView'
import LiveScoreView from './pages/captain/LiveScoreView'
import Scorecards from './pages/captain/Scorecards'
import Stats from './pages/captain/Stats'

function App() {
  const { user, isAuthenticated } = useAuthStore()

  return (
    <Router>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <Login /> : <Navigate to="/" />} />
        
        {isAuthenticated && user?.role === 'organizer' && (
          <>
            <Route path="/" element={<OrganizerLayout />}>
              <Route index element={<OrganizerDashboard />} />
              <Route path="teams" element={<TeamsManagement />} />
              <Route path="schedule" element={<MatchScheduler />} />
              <Route path="scoring" element={<LiveScoring />} />
              <Route path="points" element={<PointsTable />} />
              <Route path="knockout" element={<KnockoutBracket />} />
            </Route>
          </>
        )}
        
        {isAuthenticated && user?.role === 'captain' && (
          <>
            <Route path="/" element={<CaptainLayout />}>
              <Route index element={<CaptainDashboard />} />
              <Route path="team" element={<TeamInfo />} />
              <Route path="schedule" element={<ScheduleView />} />
              <Route path="live" element={<LiveScoreView />} />
              <Route path="scorecards" element={<Scorecards />} />
              <Route path="stats" element={<Stats />} />
            </Route>
          </>
        )}
        
        <Route path="*" element={<Navigate to={isAuthenticated ? "/" : "/login"} />} />
      </Routes>
    </Router>
  )
}

export default App

