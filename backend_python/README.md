# Cricket Tournament Management API - Python/FastAPI Backend

This is the Python/FastAPI backend migrated from the .NET 8 Web API. All API contracts, endpoints, and business logic have been preserved.

## Architecture

The backend follows a clean architecture pattern:
- **Routers** (API endpoints) → **Services** (business logic) → **Repositories** (data access)
- Uses Firebase Firestore as the database (same as .NET backend)
- Firebase Admin SDK for server-side operations
- FCM (Firebase Cloud Messaging) for notifications

## Project Structure

```
backend_python/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entrypoint
│   ├── config.py            # Settings/environment variables
│   ├── database.py           # Firebase initialization
│   ├── schemas/             # Pydantic models (DTOs)
│   │   ├── tournament.py
│   │   ├── team.py
│   │   ├── match.py
│   │   ├── points_table.py
│   │   ├── auth.py
│   │   └── notification.py
│   ├── repositories/        # Firestore data access
│   │   ├── firestore_repository.py
│   │   ├── tournament_repository.py
│   │   ├── team_repository.py
│   │   ├── match_repository.py
│   │   └── points_table_repository.py
│   ├── services/            # Business logic
│   │   ├── tournament_service.py
│   │   ├── team_service.py
│   │   ├── match_service.py
│   │   ├── points_table_service.py
│   │   ├── auth_service.py
│   │   └── notification_service.py
│   ├── routers/             # API route handlers
│   │   ├── tournaments.py
│   │   ├── teams.py
│   │   ├── matches.py
│   │   ├── auth.py
│   │   ├── points_table.py
│   │   └── notifications.py
│   ├── middleware/          # Error handling, logging
│   │   └── error_handler.py
│   └── auth/                # Auth utilities (if needed)
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- Firebase project with Firestore enabled
- Firebase service account key (JSON file)
- FCM server key (for notifications)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Firebase configuration
```

4. Update `.env` with your settings:
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=path-to-service-account-key.json
FCM_SERVER_KEY=your-fcm-server-key
DEBUG=True
```

5. Place your Firebase service account key JSON file in the project directory or provide the full path in `FIREBASE_CREDENTIALS_PATH`.

## Running the Application

### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

Or use the built-in runner:
```bash
python -m app.main
```

### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4
```

The API will be available at `http://localhost:5000`

- API Documentation: `http://localhost:5000/swagger` (when DEBUG=True)
- ReDoc: `http://localhost:5000/redoc` (when DEBUG=True)

## API Endpoints

All endpoints match the .NET backend exactly:

### Tournaments
- `POST /api/tournaments` - Create tournament
- `GET /api/tournaments` - Get all tournaments
- `GET /api/tournaments/{id}` - Get tournament by ID
- `PUT /api/tournaments/{id}` - Update tournament
- `DELETE /api/tournaments/{id}` - Delete tournament

### Teams
- `POST /api/teams` - Create team
- `GET /api/teams/{id}` - Get team by ID
- `GET /api/teams/tournament/{tournamentId}` - Get teams by tournament
- `PUT /api/teams/{id}` - Update team
- `DELETE /api/teams/{id}` - Delete team

### Matches
- `POST /api/matches` - Create match
- `GET /api/matches/{id}` - Get match by ID
- `GET /api/matches/tournament/{tournamentId}` - Get matches by tournament
- `PUT /api/matches/{id}` - Update match
- `DELETE /api/matches/{id}` - Delete match
- `POST /api/matches/{id}/score` - Update match score
- `POST /api/matches/{id}/ball` - Add ball-by-ball entry

### Points Table
- `POST /api/pointsTable/update` - Recalculate points table
- `GET /api/pointsTable/{tournamentId}/{group}` - Get points table
- `GET /api/pointsTable/{tournamentId}` - Get all points tables

### Auth
- `POST /api/auth/validateToken` - Validate Firebase JWT token

### Notifications
- `POST /api/notifications/send` - Send FCM notification
- `POST /api/notifications/send-to-team` - Send notification to team

## Configuration

The application uses environment variables that map to the .NET `appsettings.json`:

| .NET Config | Python Env Var | Description |
|------------|---------------|-------------|
| `Firebase:ProjectId` | `FIREBASE_PROJECT_ID` | Firebase project ID |
| `Firebase:CredentialsPath` | `FIREBASE_CREDENTIALS_PATH` | Path to service account key |
| `FCM:ServerKey` | `FCM_SERVER_KEY` | FCM server key for notifications |

## Testing

Run tests with pytest:
```bash
pytest
```

## Migration Notes

- All API contracts are preserved (same routes, methods, request/response shapes)
- Business logic is faithfully ported from .NET (e.g., NRR calculation)
- Error handling mirrors the .NET middleware behavior
- CORS is configured to allow all origins (matches .NET "AllowAll" policy)
- Firebase Admin SDK initialization matches .NET behavior
- FCM notifications use pyfcm library (equivalent to FCM.Net in .NET)

## Differences from .NET

1. **Async/Await**: Python uses native async/await (similar to .NET)
2. **Dependency Injection**: FastAPI's dependency system (similar to .NET DI)
3. **Validation**: Pydantic models (similar to .NET Data Annotations)
4. **Error Handling**: FastAPI exception handlers (similar to .NET middleware)
5. **Logging**: Python logging module (similar to .NET ILogger)

## Deployment

The application can be deployed using:
- Docker (create Dockerfile)
- Cloud platforms (GCP, AWS, Azure)
- Traditional servers with uvicorn/gunicorn

Example Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

## License

Same as the original .NET project.

