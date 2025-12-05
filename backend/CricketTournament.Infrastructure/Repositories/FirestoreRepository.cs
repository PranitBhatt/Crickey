using CricketTournament.Domain.Interfaces;
using Google.Cloud.Firestore;
using FirebaseAdmin;

namespace CricketTournament.Infrastructure.Repositories;

public class FirestoreRepository : IFirestoreRepository
{
    private readonly FirestoreDb _db;

    public FirestoreRepository()
    {
        _db = FirestoreDb.Create(FirebaseAdmin.FirebaseApp.DefaultInstance.ProjectId);
    }

    public async Task<T?> GetDocumentAsync<T>(string collection, string documentId) where T : class
    {
        var docRef = _db.Collection(collection).Document(documentId);
        var snapshot = await docRef.GetSnapshotAsync();
        
        if (!snapshot.Exists) return null;
        
        return snapshot.ConvertTo<T>();
    }

    public async Task<string> CreateDocumentAsync<T>(string collection, T document, string? documentId = null) where T : class
    {
        var collectionRef = _db.Collection(collection);
        DocumentReference docRef;

        if (string.IsNullOrEmpty(documentId))
        {
            docRef = await collectionRef.AddAsync(document);
        }
        else
        {
            docRef = collectionRef.Document(documentId);
            await docRef.SetAsync(document);
        }

        return docRef.Id;
    }

    public async Task UpdateDocumentAsync<T>(string collection, string documentId, T document) where T : class
    {
        var docRef = _db.Collection(collection).Document(documentId);
        await docRef.SetAsync(document, SetOptions.MergeAll);
    }

    public async Task DeleteDocumentAsync(string collection, string documentId)
    {
        var docRef = _db.Collection(collection).Document(documentId);
        await docRef.DeleteAsync();
    }

    public async Task<List<T>> GetDocumentsAsync<T>(string collection, string? field = null, object? value = null) where T : class
    {
        var query = _db.Collection(collection);

        if (!string.IsNullOrEmpty(field) && value != null)
        {
            query = query.WhereEqualTo(field, value);
        }

        var snapshot = await query.GetSnapshotAsync();
        return snapshot.Documents.Select(doc => doc.ConvertTo<T>()).ToList();
    }
}

