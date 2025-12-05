using CricketTournament.Domain.Entities;
using CricketTournament.Domain.Interfaces;
using Google.Cloud.Firestore;
using FirebaseAdmin;

namespace CricketTournament.Infrastructure.Repositories;

public class MatchRepository : IMatchRepository
{
    private readonly IFirestoreRepository _firestoreRepository;
    private readonly FirestoreDb _db;
    private const string Collection = "matches";

    public MatchRepository(IFirestoreRepository firestoreRepository)
    {
        _firestoreRepository = firestoreRepository;
        _db = FirestoreDb.Create(FirebaseAdmin.FirebaseApp.DefaultInstance.ProjectId);
    }

    public async Task<string> CreateAsync(Match match)
    {
        var data = ConvertToDictionary(match);
        return await _firestoreRepository.CreateDocumentAsync(Collection, data);
    }

    public async Task<Match?> GetByIdAsync(string id)
    {
        var data = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>(Collection, id);
        return data == null ? null : ConvertFromDictionary(id, data);
    }

    public async Task<List<Match>> GetByTournamentIdAsync(string tournamentId)
    {
        var documents = await _firestoreRepository.GetDocumentsAsync<Dictionary<string, object>>(Collection, "tournamentId", tournamentId);
        return documents.Select(doc => ConvertFromDictionary(doc["id"]?.ToString() ?? string.Empty, doc)).ToList();
    }

    public async Task UpdateAsync(Match match)
    {
        var data = ConvertToDictionary(match);
        await _firestoreRepository.UpdateDocumentAsync(Collection, match.Id, data);
    }

    public async Task DeleteAsync(string id)
    {
        await _firestoreRepository.DeleteDocumentAsync(Collection, id);
    }

    public async Task UpdateScoreAsync(string matchId, string teamId, int runs, int wickets, double overs)
    {
        var match = await GetByIdAsync(matchId);
        if (match == null) return;

        match.Scores ??= new Dictionary<string, MatchScore>();
        match.Scores[teamId] = new MatchScore
        {
            Runs = runs,
            Wickets = wickets,
            Overs = overs
        };

        await UpdateAsync(match);
    }

    public async Task AddBallByBallAsync(string matchId, BallByBall ball)
    {
        var ballData = new Dictionary<string, object>
        {
            { "ballNumber", ball.BallNumber },
            { "overNumber", ball.OverNumber },
            { "batsman", ball.Batsman },
            { "bowler", ball.Bowler },
            { "runs", ball.Runs },
            { "isWicket", ball.IsWicket },
            { "extras", ball.Extras },
            { "timestamp", Timestamp.FromDateTime(ball.Timestamp.ToUniversalTime()) }
        };

        var ballByBallRef = _db.Collection(Collection).Document(matchId).Collection("ballByBall");
        await ballByBallRef.AddAsync(ballData);
    }

    private static Dictionary<string, object> ConvertToDictionary(Match match)
    {
        var data = new Dictionary<string, object>
        {
            { "tournamentId", match.TournamentId },
            { "group", match.Group },
            { "matchNumber", match.MatchNumber },
            { "team1Id", match.Team1Id },
            { "team2Id", match.Team2Id },
            { "dateTime", Timestamp.FromDateTime(match.DateTime.ToUniversalTime()) },
            { "venue", match.Venue },
            { "overs", match.Overs },
            { "status", match.Status }
        };

        if (!string.IsNullOrEmpty(match.WinnerTeamId))
        {
            data["winnerTeamId"] = match.WinnerTeamId;
        }

        if (match.Scores != null)
        {
            var scoresDict = new Dictionary<string, object>();
            foreach (var score in match.Scores)
            {
                scoresDict[score.Key] = new Dictionary<string, object>
                {
                    { "runs", score.Value.Runs },
                    { "wickets", score.Value.Wickets },
                    { "overs", score.Value.Overs }
                };
            }
            data["scores"] = scoresDict;
        }

        return data;
    }

    private static Match ConvertFromDictionary(string id, Dictionary<string, object> data)
    {
        var match = new Match
        {
            Id = id,
            TournamentId = data["tournamentId"]?.ToString() ?? string.Empty,
            Group = data["group"]?.ToString() ?? string.Empty,
            MatchNumber = Convert.ToInt32(data["matchNumber"]),
            Team1Id = data["team1Id"]?.ToString() ?? string.Empty,
            Team2Id = data["team2Id"]?.ToString() ?? string.Empty,
            DateTime = ((Timestamp)data["dateTime"]!).ToDateTime(),
            Venue = data["venue"]?.ToString() ?? string.Empty,
            Overs = Convert.ToInt32(data["overs"]),
            Status = data["status"]?.ToString() ?? "scheduled",
            WinnerTeamId = data.ContainsKey("winnerTeamId") ? data["winnerTeamId"]?.ToString() : null
        };

        if (data.ContainsKey("scores") && data["scores"] is Dictionary<string, object> scoresDict)
        {
            match.Scores = new Dictionary<string, MatchScore>();
            foreach (var score in scoresDict)
            {
                var scoreData = (Dictionary<string, object>)score.Value;
                match.Scores[score.Key] = new MatchScore
                {
                    Runs = Convert.ToInt32(scoreData["runs"]),
                    Wickets = Convert.ToInt32(scoreData["wickets"]),
                    Overs = Convert.ToDouble(scoreData["overs"])
                };
            }
        }

        return match;
    }
}

