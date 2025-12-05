using CricketTournament.Domain.Entities;

namespace CricketTournament.Domain.Interfaces;

public interface ITeamRepository
{
    Task<string> CreateAsync(Team team);
    Task<Team?> GetByIdAsync(string id);
    Task<List<Team>> GetByTournamentIdAsync(string tournamentId);
    Task UpdateAsync(Team team);
    Task DeleteAsync(string id);
}

