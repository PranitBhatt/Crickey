# Migration Notes: .NET to Python/FastAPI

This document details the migration from .NET 8 Web API to Python 3 + FastAPI.

## Architecture Mapping

### .NET Structure → Python Structure

| .NET | Python | Notes |
|------|--------|-------|
| `Controllers/` | `routers/` | FastAPI route handlers |
| `Services/` | `services/` | Business logic layer |
| `Repositories/` | `repositories/` | Data access layer |
| `DTOs/` | `schemas/` | Pydantic models |
| `Entities/` | N/A | Direct dict handling for Firestore |
| `Middleware/` | `middleware/` | Error handlers |
| `Program.cs` | `main.py` | Application entrypoint |
| `appsettings.json` | `.env` + `config.py` | Configuration |

## Key Changes

### 1. Dependency Injection

**.NET:**
```csharp
builder.Services.AddScoped<ITournamentService, TournamentService>();
```

**Python:**
```python
def get_tournament_service(db: firestore.Client = Depends(get_db)) -> TournamentService:
    repo = TournamentRepository(db)
    return TournamentService(repo)
```

### 2. Data Transfer Objects

**.NET:**
```csharp
public class TournamentDTO
{
    public string Name { get; set; } = string.Empty;
    public DateTime StartDate { get; set; }
}
```

**Python:**
```python
class TournamentDTO(BaseModel):
    name: str = Field(..., min_length=1)
    startDate: datetime
```

### 3. Repository Pattern

**.NET:**
```csharp
public async Task<string> CreateAsync(Tournament tournament)
{
    var data = ConvertToDictionary(tournament);
    return await _firestoreRepository.CreateDocumentAsync(Collection, data);
}
```

**Python:**
```python
async def create(self, tournament: dict) -> str:
    doc_data = self._convert_to_dict(tournament)
    doc_ref = self.db.collection(self.COLLECTION).document()
    doc_ref.set(doc_data)
    return doc_ref.id
```

### 4. Error Handling

**.NET:**
```csharp
public class ErrorHandlingMiddleware
{
    public async Task InvokeAsync(HttpContext context)
    {
        try {
            await _next(context);
        } catch (Exception ex) {
            await HandleExceptionAsync(context, ex);
        }
    }
}
```

**Python:**
```python
@app.exception_handler(Exception)
async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
```

### 5. Firebase Initialization

**.NET:**
```csharp
var credential = GoogleCredential.FromFile(credentialsPath);
FirebaseApp.Create(new AppOptions {
    Credential = credential,
    ProjectId = projectId
});
```

**Python:**
```python
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {'projectId': project_id})
```

### 6. FCM Notifications

**.NET:**
```csharp
var message = new Message {
    To = token,
    Notification = new Notification { Title = title, Body = body },
    Data = data
};
await _fcmServer.SendAsync(message);
```

**Python:**
```python
message = messaging.Message(
    notification=messaging.Notification(title=title, body=body),
    data=data or {},
    token=token
)
response = messaging.send(message)
```

## API Contract Preservation

All endpoints maintain the same:
- HTTP methods (GET, POST, PUT, DELETE)
- Route paths (`/api/tournaments`, `/api/teams`, etc.)
- Request/response shapes
- Status codes (200, 204, 404, etc.)

## Business Logic Preservation

- **Net Run Rate calculation**: Identical algorithm
- **Points calculation**: Same formula (won * 2 + tied)
- **Match scoring**: Same structure and validation
- **Ball-by-ball**: Same data model

## Configuration Mapping

| .NET Config | Python Env Var |
|------------|---------------|
| `Firebase:ProjectId` | `FIREBASE_PROJECT_ID` |
| `Firebase:CredentialsPath` | `FIREBASE_CREDENTIALS_PATH` |
| `FCM:ServerKey` | `FCM_SERVER_KEY` |

## Testing Considerations

The Python backend can be tested with:
- `pytest` for unit tests
- `httpx` for integration tests
- FastAPI's `TestClient` for API tests

## Performance Notes

- Python/FastAPI is async-native (similar to .NET async/await)
- Firestore operations are synchronous in the Python SDK (but wrapped in async functions)
- Consider using `asyncio` for concurrent operations if needed

## Deployment

The Python backend can be deployed using:
- Docker (Dockerfile provided)
- Cloud Run, App Engine, or Compute Engine (GCP)
- Any platform supporting Python 3.10+

## Known Differences

1. **Type System**: Python uses dynamic typing with type hints (vs C# static typing)
2. **Null Handling**: Python uses `None` (vs C# nullable types)
3. **Collections**: Python uses `list`/`dict` (vs C# `List`/`Dictionary`)
4. **Async**: Both use async/await, but Python's Firestore SDK is synchronous

## Future Improvements

- Add comprehensive unit tests
- Add integration tests for all endpoints
- Consider async Firestore client if available
- Add request/response logging middleware
- Add rate limiting if needed
- Add API versioning if required

