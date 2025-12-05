# Setup Guide

## Quick Start

### 1. Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com
2. Enable Firestore Database
3. Enable Firebase Authentication (Email/Password)
4. Enable Firebase Cloud Messaging
5. Download service account key:
   - Go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env
# Edit .env with your Firebase config
npm run dev
```

### 3. Backend Setup

```bash
cd backend/CricketTournament.API
# Place your service-account-key.json in this directory
# Edit appsettings.json with your Firebase project ID and credentials path
dotnet restore
dotnet run
```

### 4. Seed Data (Optional)

```bash
cd scripts
npm install
# Edit seed-data.js with your service account key path
node seed-data.js
```

## Configuration

### Frontend Environment Variables

Create `frontend/.env`:

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

### Backend Configuration

Edit `backend/CricketTournament.API/appsettings.json`:

```json
{
  "Firebase": {
    "ProjectId": "your-project-id",
    "CredentialsPath": "service-account-key.json"
  },
  "FCM": {
    "ServerKey": "your-fcm-server-key"
  }
}
```

## Testing the Application

1. Start the backend: `cd backend/CricketTournament.API && dotnet run`
2. Start the frontend: `cd frontend && npm run dev`
3. Open http://localhost:3000
4. Sign up as an organizer
5. Create a tournament
6. Add teams
7. Matches will be auto-generated

## Troubleshooting

### Firebase Connection Issues
- Verify your service account key is in the correct location
- Check that Firestore is enabled in Firebase Console
- Ensure authentication is enabled

### CORS Issues
- The backend has CORS enabled for all origins in development
- For production, update the CORS policy in `Program.cs`

### Build Errors
- Ensure .NET 8 SDK is installed
- Run `dotnet restore` in the backend directory
- Run `npm install` in the frontend directory

