using CricketTournament.Application.DTOs;

namespace CricketTournament.Application.Interfaces;

public interface IPointsTableService
{
    Task UpdatePointsTableAsync(string tournamentId);
    Task<PointsTableDTO?> GetPointsTableAsync(string tournamentId, string group);
    Task<List<PointsTableDTO>> GetAllPointsTablesAsync(string tournamentId);
}

