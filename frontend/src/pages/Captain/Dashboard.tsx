import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { signOutUser } from '../../services/authService';
import { getTeamByCaptain, Team } from '../../services/teamService';
import { getMatchesByTeam, Match } from '../../services/matchService';
import { getTournament, Tournament } from '../../services/tournamentService';
import { getPointsTable, PointsTable } from '../../services/pointsTableService';
import { showToast } from '../../components/Toast';
import { CardSkeleton } from '../../components/LoadingSkeleton';
import { format } from 'date-fns';
import { LogOut, Trophy, Calendar, Users, Activity } from 'lucide-react';

export const CaptainDashboard = () => {
  const { user, profile, clearAuth } = useAuthStore();
  const [team, setTeam] = useState<Team | null>(null);
  const [tournament, setTournament] = useState<Tournament | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);
  const [pointsTable, setPointsTable] = useState<PointsTable | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      if (!user?.uid) return;

      try {
        const teamData = await getTeamByCaptain(user.uid);
        if (!teamData) {
          showToast.error('No team found for your account');
          setLoading(false);
          return;
        }

        setTeam(teamData);

        const [tournamentData, matchesData, pointsData] = await Promise.all([
          getTournament(teamData.tournamentId),
          getMatchesByTeam(teamData.id),
          getPointsTable(teamData.tournamentId, teamData.group),
        ]);

        setTournament(tournamentData);
        setMatches(matchesData);
        setPointsTable(pointsData);
      } catch (error) {
        showToast.error('Failed to load team data');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [user]);

  const handleSignOut = async () => {
    try {
      await signOutUser();
      clearAuth();
      showToast.success('Signed out successfully');
    } catch (error) {
      showToast.error('Failed to sign out');
    }
  };

  const upcomingMatches = matches.filter((m) => m.status === 'scheduled');
  const liveMatches = matches.filter((m) => m.status === 'live');
  const completedMatches = matches.filter((m) => m.status === 'completed');

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <CardSkeleton />
        </div>
      </div>
    );
  }

  if (!team) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">No team assigned to your account</p>
          <button
            onClick={handleSignOut}
            className="text-primary-600 hover:text-primary-700"
          >
            Sign Out
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Captain Dashboard</h1>
              <p className="text-sm text-gray-600">
                {team.name} - {tournament?.name || 'Tournament'}
              </p>
            </div>
            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:text-gray-900"
            >
              <LogOut className="w-4 h-4" />
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Team Info Card */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Team Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <div className="text-sm text-gray-600">Team Name</div>
              <div className="text-lg font-semibold text-gray-900">{team.name}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Group</div>
              <div className="text-lg font-semibold text-gray-900">Group {team.group}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Players</div>
              <div className="text-lg font-semibold text-gray-900">{team.players.length}</div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Upcoming Matches</div>
                <div className="text-2xl font-bold text-gray-900">{upcomingMatches.length}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3">
              <div className="bg-red-100 p-3 rounded-lg">
                <Activity className="w-6 h-6 text-red-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Live Matches</div>
                <div className="text-2xl font-bold text-gray-900">{liveMatches.length}</div>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center gap-3">
              <div className="bg-green-100 p-3 rounded-lg">
                <Trophy className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="text-sm text-gray-600">Completed</div>
                <div className="text-2xl font-bold text-gray-900">{completedMatches.length}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Live Matches */}
        {liveMatches.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Live Matches</h2>
            <div className="space-y-4">
              {liveMatches.map((match) => (
                <Link
                  key={match.id}
                  to={`/captain/matches/${match.id}`}
                  className="block border border-gray-200 rounded-lg p-4 hover:bg-gray-50"
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-semibold text-gray-900">
                        Match {match.matchNumber}
                      </div>
                      <div className="text-sm text-gray-600">
                        {format(match.dateTime, 'MMM dd, yyyy HH:mm')}
                      </div>
                    </div>
                    <span className="px-2 py-1 bg-red-100 text-red-800 rounded-full text-xs font-medium">
                      LIVE
                    </span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Upcoming Matches */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Upcoming Matches</h2>
          <div className="space-y-4">
            {upcomingMatches.length === 0 ? (
              <p className="text-gray-600 text-center py-4">No upcoming matches</p>
            ) : (
              upcomingMatches.map((match) => (
                <div
                  key={match.id}
                  className="border border-gray-200 rounded-lg p-4"
                >
                  <div className="font-semibold text-gray-900 mb-2">
                    Match {match.matchNumber}
                  </div>
                  <div className="text-sm text-gray-600">
                    {format(match.dateTime, 'MMM dd, yyyy HH:mm')} - {match.venue}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Points Table */}
        {pointsTable && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Points Table - Group {pointsTable.group}</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Team
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                      P
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                      W
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                      L
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                      Points
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">
                      NRR
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {pointsTable.entries
                    .sort((a, b) => b.points - a.points || b.netRunRate - a.netRunRate)
                    .map((entry) => (
                      <tr
                        key={entry.teamId}
                        className={entry.teamId === team.id ? 'bg-primary-50' : ''}
                      >
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">
                          {entry.teamName}
                        </td>
                        <td className="px-4 py-3 text-sm text-center text-gray-500">
                          {entry.played}
                        </td>
                        <td className="px-4 py-3 text-sm text-center text-gray-500">
                          {entry.won}
                        </td>
                        <td className="px-4 py-3 text-sm text-center text-gray-500">
                          {entry.lost}
                        </td>
                        <td className="px-4 py-3 text-sm text-center font-medium text-gray-900">
                          {entry.points}
                        </td>
                        <td className="px-4 py-3 text-sm text-center text-gray-500">
                          {entry.netRunRate.toFixed(3)}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

