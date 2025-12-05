import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getTournament, subscribeToTournament, Tournament } from '../../services/tournamentService';
import { getTeams, subscribeToTeams, Team } from '../../services/teamService';
import { getMatches, subscribeToMatches, Match } from '../../services/matchService';
import { getAllPointsTables, PointsTable } from '../../services/pointsTableService';
import { showToast } from '../../components/Toast';
import { CardSkeleton, TableSkeleton } from '../../components/LoadingSkeleton';
import { format } from 'date-fns';
import { ArrowLeft, Plus, Users, Calendar, Trophy } from 'lucide-react';

export const TournamentDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [tournament, setTournament] = useState<Tournament | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [matches, setMatches] = useState<Match[]>([]);
  const [pointsTables, setPointsTables] = useState<PointsTable[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'teams' | 'matches' | 'points'>('overview');

  useEffect(() => {
    if (!id) return;

    const loadData = async () => {
      try {
        const [tournamentData, teamsData, matchesData, pointsData] = await Promise.all([
          getTournament(id),
          getTeams(id),
          getMatches(id),
          getAllPointsTables(id),
        ]);

        setTournament(tournamentData);
        setTeams(teamsData);
        setMatches(matchesData);
        setPointsTables(pointsData);
      } catch (error) {
        showToast.error('Failed to load tournament data');
      } finally {
        setLoading(false);
      }
    };

    loadData();

    // Subscribe to real-time updates
    const unsubscribeTournament = subscribeToTournament(id, setTournament);
    const unsubscribeTeams = subscribeToTeams(id, setTeams);
    const unsubscribeMatches = subscribeToMatches(id, setMatches);

    return () => {
      unsubscribeTournament();
      unsubscribeTeams();
      unsubscribeMatches();
    };
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <CardSkeleton />
        </div>
      </div>
    );
  }

  if (!tournament) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-600">Tournament not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link
          to="/organizer"
          className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Dashboard
        </Link>

        {/* Tournament Header */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{tournament.name}</h1>
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <span className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  {format(tournament.startDate, 'MMM dd')} -{' '}
                  {format(tournament.endDate, 'MMM dd, yyyy')}
                </span>
                <span>{tournament.location}</span>
                <span className="px-2 py-1 bg-primary-100 text-primary-800 rounded-full text-xs font-medium">
                  {tournament.status}
                </span>
              </div>
            </div>
            <div className="flex gap-2">
              <Link
                to={`/organizer/tournaments/${id}/teams/add`}
                className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
              >
                <Plus className="w-4 h-4" />
                Add Team
              </Link>
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {[
                { id: 'overview', label: 'Overview' },
                { id: 'teams', label: 'Teams' },
                { id: 'matches', label: 'Matches' },
                { id: 'points', label: 'Points Table' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-6 py-3 text-sm font-medium border-b-2 ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-primary-50 rounded-lg p-4">
                  <div className="text-sm text-primary-600 font-medium">Total Teams</div>
                  <div className="text-2xl font-bold text-primary-900">{teams.length}</div>
                </div>
                <div className="bg-green-50 rounded-lg p-4">
                  <div className="text-sm text-green-600 font-medium">Total Matches</div>
                  <div className="text-2xl font-bold text-green-900">{matches.length}</div>
                </div>
                <div className="bg-blue-50 rounded-lg p-4">
                  <div className="text-sm text-blue-600 font-medium">Groups</div>
                  <div className="text-2xl font-bold text-blue-900">{tournament.groups.length}</div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'teams' && (
            <div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {teams.map((team) => (
                  <div key={team.id} className="border border-gray-200 rounded-lg p-4">
                    <h3 className="font-semibold text-gray-900 mb-2">{team.name}</h3>
                    <div className="text-sm text-gray-600 space-y-1">
                      <div>Group: {team.group}</div>
                      <div>Captain: {team.captainName}</div>
                      <div>Players: {team.players.length}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'matches' && (
            <div>
              <div className="space-y-4">
                {matches.map((match) => (
                  <div
                    key={match.id}
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
                    onClick={() => navigate(`/organizer/matches/${match.id}/score`)}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-semibold text-gray-900">
                          Match {match.matchNumber} - Group {match.group}
                        </div>
                        <div className="text-sm text-gray-600">
                          {format(match.dateTime, 'MMM dd, yyyy HH:mm')} - {match.venue}
                        </div>
                      </div>
                      <span
                        className={`px-2 py-1 text-xs font-medium rounded-full ${
                          match.status === 'live'
                            ? 'bg-red-100 text-red-800'
                            : match.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {match.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'points' && (
            <div className="space-y-6">
              {pointsTables.map((table) => (
                <div key={table.group}>
                  <h3 className="text-lg font-semibold mb-4">Group {table.group}</h3>
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
                        {table.entries
                          .sort((a, b) => b.points - a.points || b.netRunRate - a.netRunRate)
                          .map((entry) => (
                            <tr key={entry.teamId}>
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
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

