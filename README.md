# Cricket Tournament Management System

A complete, production-ready cricket tournament management application with a futuristic UI theme.

## 🎯 Features

- **Tournament Management**: Create and manage tournaments with 12 teams, 2 groups
- **Auto Scheduling**: Automatic match schedule generation
- **Live Scoring**: Real-time ball-by-ball scoring
- **Points Table**: Automatic calculation with Net Run Rate (NRR)
- **Knockout Management**: Auto-generate semi-finals and final
- **Role-Based Access**: Organizer and Captain roles
- **Futuristic UI**: Hyper-tech theme with neon blue accents

## 🏗️ Architecture

- **Frontend**: React + Vite + TypeScript + TailwindCSS
- **Backend**: Python FastAPI + SQLAlchemy + PostgreSQL
- **Deployment**: Frontend (Vercel) + Backend (Render)

## 📦 Setup Instructions

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend_python
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**:
   - Create a PostgreSQL database (local or Google Cloud SQL)
   - Update `DATABASE_URL` in `.env` file

5. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run database migrations** (if using Alembic):
   ```bash
   alembic upgrade head
   ```

7. **Start the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment variables**:
   Create `.env` file:
   ```env
   VITE_API_BASE_URL=http://localhost:5000/api
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

## 🚀 Deployment

### Backend (Render)

1. **Create a new Web Service on Render**
2. **Connect your repository**
3. **Set build command**: `pip install -r requirements.txt`
4. **Set start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Add environment variables**:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: A secure random string
   - `DEBUG`: `False`
   - `CORS_ORIGINS`: Your Vercel frontend URL

### Frontend (Vercel)

1. **Import your repository to Vercel**
2. **Set root directory**: `frontend`
3. **Add environment variable**:
   - `VITE_API_BASE_URL`: Your Render backend URL (e.g., `https://your-app.onrender.com/api`)
4. **Deploy**

## 📁 Project Structure

```
backend_python/
├── app/
│   ├── auth/          # Authentication dependencies
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   ├── routers/       # API endpoints
│   ├── middleware/    # Error handling
│   ├── config.py      # Configuration
│   ├── database.py    # Database setup
│   └── main.py        # FastAPI app
├── requirements.txt
├── Dockerfile
└── .env.example

frontend/
├── src/
│   ├── components/    # Reusable UI components
│   ├── layouts/       # Layout components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── store/         # Zustand stores
│   └── App.tsx
├── package.json
└── vite.config.ts
```

## 🔐 Authentication

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control (Organizer/Captain)

## 🎨 UI Theme

- **Colors**: Black background with neon blue accents (#00b7ff)
- **Effects**: Glassmorphism, glowing borders, smooth transitions
- **Components**: Glass cards, neon buttons, futuristic styling

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Tournaments
- `GET /api/tournaments` - List all tournaments
- `POST /api/tournaments` - Create tournament (Organizer)
- `GET /api/tournaments/{id}` - Get tournament
- `PUT /api/tournaments/{id}` - Update tournament (Organizer)
- `DELETE /api/tournaments/{id}` - Delete tournament (Organizer)

### Teams
- `GET /api/teams/tournament/{id}` - Get teams by tournament
- `POST /api/teams` - Create team (Organizer)
- `GET /api/teams/{id}` - Get team
- `PUT /api/teams/{id}` - Update team (Organizer)
- `DELETE /api/teams/{id}` - Delete team (Organizer)

### Matches
- `GET /api/matches/tournament/{id}` - Get matches by tournament
- `POST /api/matches` - Create match (Organizer)
- `POST /api/matches/{id}/score` - Update score (Organizer)
- `POST /api/matches/{id}/ball` - Add ball-by-ball (Organizer)

### Schedule
- `POST /api/schedule/generate-group-stage` - Generate group stage (Organizer)
- `POST /api/schedule/generate-knockout` - Generate knockout (Organizer)

### Points Table
- `POST /api/points-table/calculate/{tournament_id}/{group}` - Calculate points
- `GET /api/points-table/{tournament_id}/{group}` - Get points table

## 🧪 Testing

### Backend
```bash
# Run tests (when implemented)
pytest
```

### Frontend
```bash
# Run tests (when implemented)
npm test
```

## 📄 License

MIT

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

