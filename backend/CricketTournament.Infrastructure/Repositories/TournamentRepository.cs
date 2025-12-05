using CricketTournament.Domain.Entities;
using CricketTournament.Domain.Interfaces;
using Google.Cloud.Firestore;
using System.Collections;

namespace CricketTournament.Infrastructure.Repositories;

public class TournamentRepository : ITournamentRepository
{
    private readonly IFirestoreRepository _firestoreRepository;
    private const string Collection = "tournaments";

    public TournamentRepository(IFirestoreRepository firestoreRepository)
    {
        _firestoreRepository = firestoreRepository;
    }

    public async Task<string> CreateAsync(Tournament tournament)
    {
        var data = ConvertToDictionary(tournament);
        return await _firestoreRepository.CreateDocumentAsync(Collection, data);
    }

    public async Task<Tournament?> GetByIdAsync(string id)
    {
        var data = await _firestoreRepository.GetDocumentAsync<Dictionary<string, object>>(Collection, id);
        return data == null ? null : ConvertFromDictionary(id, data);
    }

    public async Task<List<Tournament>> GetAllAsync()
    {
        var documents = await _firestoreRepository.GetDocumentsAsync<Dictionary<string, object>>(Collection);
        return documents.Select(doc => ConvertFromDictionary(doc["id"].ToString() ?? string.Empty, doc)).ToList();
    }

    public async Task UpdateAsync(Tournament tournament)
    {
        var data = ConvertToDictionary(tournament);
        await _firestoreRepository.UpdateDocumentAsync(Collection, tournament.Id, data);
    }

    public async Task DeleteAsync(string id)
    {
        await _firestoreRepository.DeleteDocumentAsync(Collection, id);
    }

    private static Dictionary<string, object> ConvertToDictionary(Tournament tournament)
    {
        return new Dictionary<string, object>
        {
            { "name", tournament.Name },
            { "startDate", Timestamp.FromDateTime(tournament.StartDate.ToUniversalTime()) },
            { "endDate", Timestamp.FromDateTime(tournament.EndDate.ToUniversalTime()) },
            { "location", tournament.Location },
            { "oversGroup", tournament.OversGroup },
            { "oversKnockout", tournament.OversKnockout },
            { "groups", tournament.Groups },
            { "status", tournament.Status },
            { "createdBy", tournament.CreatedBy }
        };
    }

    private static Tournament ConvertFromDictionary(string id, Dictionary<string, object> data)
    {
        return new Tournament
        {
            Id = id,
            Name = data.GetValueOrDefault("name")?.ToString() ?? string.Empty,
            StartDate = ((Timestamp)data.GetValueOrDefault("startDate")!).ToDateTime(),
            EndDate = ((Timestamp)data.GetValueOrDefault("endDate")!).ToDateTime(),
            Location = data.GetValueOrDefault("location")?.ToString() ?? string.Empty,
            OversGroup = Convert.ToInt32(data.GetValueOrDefault("oversGroup")),
            OversKnockout = Convert.ToInt32(data.GetValueOrDefault("oversKnockout")),
            Groups = ((List<object>)data.GetValueOrDefault("groups")!).Select(g => g.ToString()!).ToList(),
            Status = data.GetValueOrDefault("status")?.ToString() ?? "upcoming",
            CreatedBy = data.GetValueOrDefault("createdBy")?.ToString() ?? string.Empty
        };
    }
}

