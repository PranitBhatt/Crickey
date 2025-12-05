# Cricket Tournament Management System

A full-stack cricket tournament management application built with React, .NET 8, and Firebase Firestore.

## 🏗️ Architecture

- **Frontend**: React 18 + Vite + TypeScript + TailwindCSS
- **Backend**: .NET 8 Web API with Clean Architecture
- **Database**: Firebase Firestore
- **Authentication**: Firebase Authentication
- **Real-time**: Firestore Listeners
- **Notifications**: Firebase Cloud Messaging (FCM)

## 📁 Project Structure

```
Crickey/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/          # Page components
│   │   │   ├── Organizer/  # Organizer dashboard pages
│   │   │   └── Captain/    # Captain dashboard pages
│   │   ├── services/       # API and Firebase services
│   │   ├── store/          # Zustand state management
│   │   └── routes/         # Routing configuration
│   └── package.json
│
├── backend/                 # .NET 8 Web API
│   ├── CricketTournament.API/          # API layer
│   ├── CricketTournament.Application/  # Application layer
│   ├── CricketTournament.Domain/      # Domain entities
│   └── CricketTournament.Infrastructure/ # Infrastructure layer
│
└── scripts/                 # Utility scripts
    └── seed-data.js        # Data seeding script
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- .NET 8 SDK
- Firebase project with Firestore enabled
- Firebase service account key (JSON file)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Update `.env` with your Firebase configuration:
```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_FIREBASE_VAPID_KEY=your_vapid_key
VITE_API_BASE_URL=http://localhost:5000/api
```

5. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend/CricketTournament.API
```

2. Update `appsettings.json` with your Firebase configuration:
```json
{
  "Firebase": {
    "ProjectId": "your-project-id",
    "CredentialsPath": "path-to-service-account-key.json"
  },
  "FCM": {
    "ServerKey": "your-fcm-server-key"
  }
}
```

3. Place your Firebase service account key JSON file in the API project directory.

4. Run the API:
```bash
dotnet run
```

The API will be available at `http://localhost:5000`

### Seeding Data

1. Install Node.js dependencies for the seeding script:
```bash
npm install firebase-admin
```

2. Update `scripts/seed-data.js` with the path to your service account key.

3. Run the seeding script:
```bash
node scripts/seed-data.js
```

This will create:
- 1 tournament
- 12 teams (6 in Group A, 6 in Group B)
- 21 matches
- Points table placeholders

## 🔐 Authentication

The application uses Firebase Authentication for user management. Users can sign up as either:
- **Organizer**: Can create tournaments, teams, matches, and manage scoring
- **Captain**: Can view team information, schedule, standings, and live scores

## 📊 Features

### Organizer Dashboard
- Create and manage tournaments
- Add teams and players
- Auto-generate groups and matches
- Enter live scores
- Add ball-by-ball scoring
- Update match results
- View points table
- Send notifications to team captains

### Captain Dashboard
- View team details
- See upcoming matches
- View live scores
- Check completed match scorecards
- View points table
- See players list

## 🔥 Firebase Collections

- `tournaments`: Tournament information
- `teams`: Team details and players
- `matches`: Match schedules and scores
- `matches/{matchId}/ballByBall`: Ball-by-ball scoring data
- `pointsTable`: Points table for each group
- `users`: User profiles and roles

## 📡 API Endpoints

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

## 🛠️ Development

### Frontend
- Uses Vite for fast development
- TypeScript for type safety
- TailwindCSS for styling
- Zustand for state management
- React Router for navigation

### Backend
- Clean Architecture pattern
- Dependency Injection
- AutoMapper for DTOs
- Firebase Admin SDK
- Error handling middleware

## 📝 License

This project is for educational purposes.

