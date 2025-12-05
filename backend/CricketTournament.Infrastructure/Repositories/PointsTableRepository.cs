using CricketTournament.Application.DTOs;
using CricketTournament.Domain.Interfaces;
using Google.Cloud.Firestore;
using System.Collections;

namespace CricketTournament.Infrastructure.Repositories;

public class PointsTableRepository : IPointsTableRepository
{
    private readonly IFirestoreRepository _firestoreRepository;
    private const string Collection = "pointsTable";

    public PointsTableRepository(IFirestoreRepository firestoreRepository)
    {
        _firestoreRepository = firestoreRepository;
    }

    public async Task UpsertAsync(string tournamentId, string group, PointsTableDTO pointsTable)
    {
        var data = ConvertToDictionary(pointsTable);
        var documentId = $"{tournamentId}_{group}";
        await _firestoreRepository.CreateDocumentAsync(Collection, data, documentId);
    }

    public async Task<PointsTableDTO?> GetAsync(string tournamentId, string group)
    {
        var documentId = $"{tournamentId}_{group}";
        var data = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>(Collection, documentId);
        return data == null ? null : ConvertFromDictionary(data);
    }

    public async Task<List<PointsTableDTO>> GetAllAsync(string tournamentId)
    {
        var documents = await _firestoreRepository.GetDocumentsAsync<Dictionary<string, object>>(Collection, "tournamentId", tournamentId);
        return documents.Select(ConvertFromDictionary).ToList();
    }

    private static Dictionary<string, object> ConvertToDictionary(PointsTableDTO pointsTable)
    {
        var entries = pointsTable.Entries.Select(e => new Dictionary<string, object>
        {
            { "teamId", e.TeamId },
            { "teamName", e.TeamName },
            { "group", e.Group },
            { "played", e.Played },
            { "won", e.Won },
            { "lost", e.Lost },
            { "tied", e.Tied },
            { "points", e.Points },
            { "netRunRate", e.NetRunRate },
            { "runsFor", e.RunsFor },
            { "runsAgainst", e.RunsAgainst },
            { "oversFor", e.OversFor },
            { "oversAgainst", e.OversAgainst }
        }).ToList();

        return new Dictionary<string, object>
        {
            { "tournamentId", pointsTable.TournamentId },
            { "group", pointsTable.Group },
            { "entries", entries },
            { "lastUpdated", Timestamp.FromDateTime(pointsTable.LastUpdated.ToUniversalTime()) }
        };
    }

    private static PointsTableDTO ConvertFromDictionary(Dictionary<string, object> data)
    {
        var entries = new List<PointsTableEntryDTO>();
        if (data.ContainsKey("entries") && data["entries"] is List<object> entriesList)
        {
            entries = entriesList.Select(e =>
            {
                var entryDict = (Dictionary<string, object>)e;
                return new PointsTableEntryDTO
                {
                    TeamId = entryDict["teamId"]?.ToString() ?? string.Empty,
                    TeamName = entryDict["teamName"]?.ToString() ?? string.Empty,
                    Group = entryDict["group"]?.ToString() ?? string.Empty,
                    Played = Convert.ToInt32(entryDict["played"]),
                    Won = Convert.ToInt32(entryDict["won"]),
                    Lost = Convert.ToInt32(entryDict["lost"]),
                    Tied = Convert.ToInt32(entryDict["tied"]),
                    Points = Convert.ToInt32(entryDict["points"]),
                    NetRunRate = Convert.ToDouble(entryDict["netRunRate"]),
                    RunsFor = Convert.ToInt32(entryDict["runsFor"]),
                    RunsAgainst = Convert.ToInt32(entryDict["runsAgainst"]),
                    OversFor = Convert.ToDouble(entryDict["oversFor"]),
                    OversAgainst = Convert.ToDouble(entryDict["oversAgainst"])
                };
            }).ToList();
        }

        return new PointsTableDTO
        {
            TournamentId = data["tournamentId"]?.ToString() ?? string.Empty,
            Group = data["group"]?.ToString() ?? string.Empty,
            Entries = entries,
            LastUpdated = ((Timestamp)data["lastUpdated"]!).ToDateTime()
        };
    }
}

