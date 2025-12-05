using CricketTournament.Domain.Entities;
using CricketTournament.Domain.Interfaces;
using System.Collections;

namespace CricketTournament.Infrastructure.Repositories;

public class TeamRepository : ITeamRepository
{
    private readonly IFirestoreRepository _firestoreRepository;
    private const string Collection = "teams";

    public TeamRepository(IFirestoreRepository firestoreRepository)
    {
        _firestoreRepository = firestoreRepository;
    }

    public async Task<string> CreateAsync(Team team)
    {
        var data = ConvertToDictionary(team);
        return await _firestoreRepository.CreateDocumentAsync(Collection, data);
    }

    public async Task<Team?> GetByIdAsync(string id)
    {
        var data = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>(Collection, id);
        return data == null ? null : ConvertFromDictionary(id, data);
    }

    public async Task<List<Team>> GetByTournamentIdAsync(string tournamentId)
    {
        var documents = await _firestoreRepository.GetDocumentsAsync<Dictionary<string, object>>(Collection, "tournamentId", tournamentId);
        return documents.Select(doc => ConvertFromDictionary(doc["id"]?.ToString() ?? string.Empty, doc)).ToList();
    }

    public async Task UpdateAsync(Team team)
    {
        var data = ConvertToDictionary(team);
        await _firestoreRepository.UpdateDocumentAsync(Collection, team.Id, data);
    }

    public async Task DeleteAsync(string id)
    {
        await _firestoreRepository.DeleteDocumentAsync(Collection, id);
    }

    private static Dictionary<string, object> ConvertToDictionary(Team team)
    {
        var data = new Dictionary<string, object>
        {
            { "tournamentId", team.TournamentId },
            { "name", team.Name },
            { "group", team.Group },
            { "captainName", team.CaptainName },
            { "captainUid", team.CaptainUid },
            { "logoUrl", team.LogoUrl },
            { "players", team.Players.Select(p => new Dictionary<string, object> { { "name", p.Name }, { "role", p.Role } }).ToList() }
        };

        if (team.Substitute != null)
        {
            data["substitute"] = new Dictionary<string, object> { { "name", team.Substitute.Name }, { "role", team.Substitute.Role } };
        }

        return data;
    }

    private static Team ConvertFromDictionary(string id, Dictionary<string, object> data)
    {
        var players = new List<Player>();
        if (data.ContainsKey("players") && data["players"] is List<object> playersList)
        {
            players = playersList.Select(p =>
            {
                var playerDict = (Dictionary<string, object>)p;
                return new Player
                {
                    Name = playerDict["name"]?.ToString() ?? string.Empty,
                    Role = playerDict["role"]?.ToString() ?? string.Empty
                };
            }).ToList();
        }

        Player? substitute = null;
        if (data.ContainsKey("substitute") && data["substitute"] is Dictionary<string, object> subDict)
        {
            substitute = new Player
            {
                Name = subDict["name"]?.ToString() ?? string.Empty,
                Role = subDict["role"]?.ToString() ?? string.Empty
            };
        }

        return new Team
        {
            Id = id,
            TournamentId = data["tournamentId"]?.ToString() ?? string.Empty,
            Name = data["name"]?.ToString() ?? string.Empty,
            Group = data["group"]?.ToString() ?? string.Empty,
            CaptainName = data["captainName"]?.ToString() ?? string.Empty,
            CaptainUid = data["captainUid"]?.ToString() ?? string.Empty,
            LogoUrl = data["logoUrl"]?.ToString() ?? string.Empty,
            Players = players,
            Substitute = substitute
        };
    }
}

