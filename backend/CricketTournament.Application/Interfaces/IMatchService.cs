using CricketTournament.Application.DTOs;

namespace CricketTournament.Application.Interfaces;

public interface IMatchService
{
    Task<string> CreateMatchAsync(MatchDTO match);
    Task<MatchDTO?> GetMatchAsync(string id);
    Task<List<MatchDTO>> GetMatchesByTournamentAsync(string tournamentId);
    Task UpdateMatchAsync(string id, MatchDTO match);
    Task DeleteMatchAsync(string id);
    Task UpdateMatchScoreAsync(string matchId, ScoreUpdateDTO score);
    Task AddBallByBallAsync(string matchId, BallByBallDTO ball);
}

