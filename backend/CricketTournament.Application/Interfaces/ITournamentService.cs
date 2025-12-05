using CricketTournament.Application.DTOs;

namespace CricketTournament.Application.Interfaces;

public interface ITournamentService
{
    Task<string> CreateTournamentAsync(TournamentDTO tournament);
    Task<TournamentDTO?> GetTournamentAsync(string id);
    Task<List<TournamentDTO>> GetAllTournamentsAsync();
    Task UpdateTournamentAsync(string id, TournamentDTO tournament);
    Task DeleteTournamentAsync(string id);
}

