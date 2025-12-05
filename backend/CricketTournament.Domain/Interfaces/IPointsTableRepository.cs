using CricketTournament.Application.DTOs;

namespace CricketTournament.Domain.Interfaces;

public interface IPointsTableRepository
{
    Task UpsertAsync(string tournamentId, string group, PointsTableDTO pointsTable);
    Task<PointsTableDTO?> GetAsync(string tournamentId, string group);
    Task<List<PointsTableDTO>> GetAllAsync(string tournamentId);
}

