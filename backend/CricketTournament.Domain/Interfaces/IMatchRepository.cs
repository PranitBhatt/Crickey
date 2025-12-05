using CricketTournament.Domain.Entities;

namespace CricketTournament.Domain.Interfaces;

public interface IMatchRepository
{
    Task<string> CreateAsync(Match match);
    Task<Match?> GetByIdAsync(string id);
    Task<List<Match>> GetByTournamentIdAsync(string tournamentId);
    Task UpdateAsync(Match match);
    Task DeleteAsync(string id);
    Task UpdateScoreAsync(string matchId, string teamId, int runs, int wickets, double overs);
    Task AddBallByBallAsync(string matchId, BallByBall ball);
}

