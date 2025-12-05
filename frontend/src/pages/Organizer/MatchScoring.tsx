import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getMatch, updateMatchScore, addBallByBall, Match, subscribeToMatch } from '../../services/matchService';
import { getTeam, Team } from '../../services/teamService';
import { showToast } from '../../components/Toast';
import { CardSkeleton } from '../../components/LoadingSkeleton';
import { ArrowLeft, Save } from 'lucide-react';

export const MatchScoring = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [match, setMatch] = useState<Match | null>(null);
  const [team1, setTeam1] = useState<Team | null>(null);
  const [team2, setTeam2] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [score1, setScore1] = useState({ runs: 0, wickets: 0, overs: 0 });
  const [score2, setScore2] = useState({ runs: 0, wickets: 0, overs: 0 });
  const [ballData, setBallData] = useState({
    overNumber: 1,
    ballNumber: 1,
    batsman: '',
    bowler: '',
    runs: 0,
    isWicket: false,
    extras: 0,
  });

  useEffect(() => {
    if (!id) return;

    const loadData = async () => {
      try {
        const matchData = await getMatch(id);
        if (!matchData) {
          showToast.error('Match not found');
          navigate('/organizer');
          return;
        }

        setMatch(matchData);
        setScore1(matchData.scores[matchData.team1Id] || { runs: 0, wickets: 0, overs: 0 });
        setScore2(matchData.scores[matchData.team2Id] || { runs: 0, wickets: 0, overs: 0 });

        const [team1Data, team2Data] = await Promise.all([
          getTeam(matchData.team1Id),
          getTeam(matchData.team2Id),
        ]);

        setTeam1(team1Data);
        setTeam2(team2Data);
      } catch (error) {
        showToast.error('Failed to load match data');
      } finally {
        setLoading(false);
      }
    };

    loadData();

    // Subscribe to real-time updates
    const unsubscribe = subscribeToMatch(id, (updatedMatch: Match | null) => {
      if (updatedMatch) {
        setMatch(updatedMatch);
        setScore1(updatedMatch.scores[updatedMatch.team1Id] || { runs: 0, wickets: 0, overs: 0 });
        setScore2(updatedMatch.scores[updatedMatch.team2Id] || { runs: 0, wickets: 0, overs: 0 });
      }
    });

    return () => unsubscribe();
  }, [id, navigate]);

  const handleUpdateScore = async (teamId: string, score: typeof score1) => {
    if (!id) return;
    try {
      await updateMatchScore(id, {
        teamId,
        runs: score.runs,
        wickets: score.wickets,
        overs: score.overs,
      });
      showToast.success('Score updated successfully');
    } catch (error) {
      showToast.error('Failed to update score');
    }
  };

  const handleAddBall = async () => {
    if (!id) return;
    try {
      await addBallByBall(id, {
        ballNumber: ballData.ballNumber,
        overNumber: ballData.overNumber,
        batsman: ballData.batsman,
        bowler: ballData.bowler,
        runs: ballData.runs,
        isWicket: ballData.isWicket,
        extras: ballData.extras,
      });
      showToast.success('Ball added successfully');
      // Reset ball data
      setBallData({
        ...ballData,
        ballNumber: ballData.ballNumber + 1,
        runs: 0,
        isWicket: false,
        extras: 0,
      });
    } catch (error) {
      showToast.error('Failed to add ball');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <CardSkeleton />
        </div>
      </div>
    );
  }

  if (!match || !team1 || !team2) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-600">Match not found</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link
          to={`/organizer/tournaments/${match.tournamentId}`}
          className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Tournament
        </Link>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Match {match.matchNumber} - {team1.name} vs {team2.name}
          </h1>
          <div className="text-sm text-gray-600">
            Group {match.group} • {match.venue}
          </div>
        </div>

        {/* Score Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Team 1 Score */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">{team1.name}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Runs</label>
                <input
                  type="number"
                  value={score1.runs}
                  onChange={(e) => setScore1({ ...score1, runs: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Wickets</label>
                <input
                  type="number"
                  value={score1.wickets}
                  onChange={(e) => setScore1({ ...score1, wickets: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Overs</label>
                <input
                  type="number"
                  step="0.1"
                  value={score1.overs}
                  onChange={(e) => setScore1({ ...score1, overs: parseFloat(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <button
                onClick={() => handleUpdateScore(match.team1Id, score1)}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 flex items-center justify-center gap-2"
              >
                <Save className="w-4 h-4" />
                Update Score
              </button>
            </div>
          </div>

          {/* Team 2 Score */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">{team2.name}</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Runs</label>
                <input
                  type="number"
                  value={score2.runs}
                  onChange={(e) => setScore2({ ...score2, runs: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Wickets</label>
                <input
                  type="number"
                  value={score2.wickets}
                  onChange={(e) => setScore2({ ...score2, wickets: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Overs</label>
                <input
                  type="number"
                  step="0.1"
                  value={score2.overs}
                  onChange={(e) => setScore2({ ...score2, overs: parseFloat(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <button
                onClick={() => handleUpdateScore(match.team2Id, score2)}
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 flex items-center justify-center gap-2"
              >
                <Save className="w-4 h-4" />
                Update Score
              </button>
            </div>
          </div>
        </div>

        {/* Ball-by-Ball Scoring */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Ball-by-Ball Scoring</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Over Number</label>
              <input
                type="number"
                value={ballData.overNumber}
                onChange={(e) => setBallData({ ...ballData, overNumber: parseInt(e.target.value) || 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Ball Number</label>
              <input
                type="number"
                value={ballData.ballNumber}
                onChange={(e) => setBallData({ ...ballData, ballNumber: parseInt(e.target.value) || 1 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Runs</label>
              <input
                type="number"
                value={ballData.runs}
                onChange={(e) => setBallData({ ...ballData, runs: parseInt(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Batsman</label>
              <input
                type="text"
                value={ballData.batsman}
                onChange={(e) => setBallData({ ...ballData, batsman: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bowler</label>
              <input
                type="text"
                value={ballData.bowler}
                onChange={(e) => setBallData({ ...ballData, bowler: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Extras</label>
              <input
                type="number"
                value={ballData.extras}
                onChange={(e) => setBallData({ ...ballData, extras: parseInt(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
          <div className="flex items-center gap-4 mb-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={ballData.isWicket}
                onChange={(e) => setBallData({ ...ballData, isWicket: e.target.checked })}
                className="w-4 h-4"
              />
              <span className="text-sm font-medium text-gray-700">Wicket</span>
            </label>
          </div>
          <button
            onClick={handleAddBall}
            className="bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700"
          >
            Add Ball
          </button>
        </div>
      </div>
    </div>
  );
};


