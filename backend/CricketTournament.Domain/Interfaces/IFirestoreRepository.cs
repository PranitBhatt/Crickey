namespace CricketTournament.Domain.Interfaces;

public interface IFirestoreRepository
{
    Task<T?> GetDocumentAsync<T>(string collection, string documentId) where T : class;
    Task<string> CreateDocumentAsync<T>(string collection, T document, string? documentId = null) where T : class;
    Task UpdateDocumentAsync<T>(string collection, string documentId, T document) where T : class;
    Task DeleteDocumentAsync(string collection, string documentId);
    Task<List<T>> GetDocumentsAsync<T>(string collection, string? field = null, object? value = null) where T : class;
}

