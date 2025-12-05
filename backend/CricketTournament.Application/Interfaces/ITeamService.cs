using CricketTournament.Application.DTOs;

namespace CricketTournament.Application.Interfaces;

public interface ITeamService
{
    Task<string> CreateTeamAsync(TeamDTO team);
    Task<TeamDTO?> GetTeamAsync(string id);
    Task<List<TeamDTO>> GetTeamsByTournamentAsync(string tournamentId);
    Task UpdateTeamAsync(string id, TeamDTO team);
    Task DeleteTeamAsync(string id);
}

