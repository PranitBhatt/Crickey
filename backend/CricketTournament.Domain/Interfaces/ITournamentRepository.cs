using CricketTournament.Domain.Entities;

namespace CricketTournament.Domain.Interfaces;

public interface ITournamentRepository
{
    Task<string> CreateAsync(Tournament tournament);
    Task<Tournament?> GetByIdAsync(string id);
    Task<List<Tournament>> GetAllAsync();
    Task UpdateAsync(Tournament tournament);
    Task DeleteAsync(string id);
}

