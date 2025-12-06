# Deployment Guide: Render (Backend) + Vercel (Frontend)

This guide walks you through deploying the Cricket Tournament Management application to production using Render for the Python FastAPI backend and Vercel for the React frontend.

---

## 📋 Prerequisites

1. **Firebase Project** with:
   - Authentication enabled
   - Firestore Database enabled
   - Service Account Key downloaded (`serviceAccountKey.json`)

2. **Render Account** (for backend)
   - Sign up at [render.com](https://render.com)

3. **Vercunt** (for frontend)
   - Sign up at el Acco[vercel.com](https://vercel.com)

4. **GitHub Repository** (or GitLab/Bitbucket)
   - Your code should be in a Git repository

---

## 🚀 Backend Deployment (Render)

### Step 1: Prepare Service Account Key

1. Download your Firebase Service Account Key:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `serviceAccountKey.json`

2. **⚠️ IMPORTANT**: Never commit this file to Git!
   - It's already in `.gitignore`
   - Verify: `git status` should NOT show `serviceAccountKey.json`

### Step 2: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository
4. Configure the service:

   **Basic Settings:**
   - **Name**: `cricket-tournament-api` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `backend_python` (if your backend is in a subdirectory)

   **Build & Deploy:**
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

   **⚠️ Important**: Render automatically sets the `$PORT` environment variable. Your app must use it.

### Step 3: Add Environment Variables

In Render Dashboard → Your Service → Environment:

Add the following **Environment Variables**:

| Key | Value | Description |
|-----|-------|-------------|
| `FIREBASE_PROJECT_ID` | `your-firebase-project-id` | Your Firebase project ID |
| `FIREBASE_CREDENTIALS_PATH` | `/opt/render/project/src/serviceAccountKey.json` | Path to service account key |
| `DEBUG` | `False` | Set to False for production |
| `PORT` | (auto-set by Render) | Automatically set by Render |

### Step 4: Add Secret File (serviceAccountKey.json)

1. In Render Dashboard → Your Service → **"Secret Files"** tab
2. Click **"Add Secret File"**
3. **File Path**: `serviceAccountKey.json`
4. **File Contents**: Paste the entire contents of your `serviceAccountKey.json` file
5. Click **"Save"**

   **Note**: The file will be placed at the project root, so `FIREBASE_CREDENTIALS_PATH` should point to:
   ```
   /opt/render/project/src/serviceAccountKey.json
   ```
   
   Or if your backend is in a subdirectory:
   ```
   /opt/render/project/src/backend_python/serviceAccountKey.json
   ```

### Step 5: Deploy

1. Click **"Save Changes"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start your application
3. Wait for deployment to complete (usually 2-5 minutes)
4. Your backend will be available at: `https://your-service-name.onrender.com`

### Step 6: Verify Backend Health

1. Visit: `https://your-service-name.onrender.com/health`
2. You should see: `{"status": "ok"}`
3. Visit: `https://your-service-name.onrender.com/`
4. You should see the API welcome message

**Save your backend URL** - you'll need it for frontend configuration!

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Environment Variables

Before deploying, gather these values:

1. **Firebase Configuration** (from Firebase Console → Project Settings → General):
   - `VITE_FIREBASE_API_KEY`
   - `VITE_FIREBASE_AUTH_DOMAIN`
   - `VITE_FIREBASE_PROJECT_ID`
   - `VITE_FIREBASE_STORAGE_BUCKET`
   - `VITE_FIREBASE_MESSAGING_SENDER_ID`
   - `VITE_FIREBASE_APP_ID`
   - `VITE_FIREBASE_VAPID_KEY` (for notifications, if using)

2. **Backend URL** (from Render):
   - `VITE_API_BASE_URL` = `https://your-service-name.onrender.com/api`

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

3. Login to Vercel:
   ```bash
   vercel login
   ```

4. Deploy:
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project? (No for first time)
   - Project name? (Enter your project name)
   - Directory? (Enter `frontend` or `.` if already in frontend)
   - Override settings? (No)

5. Add environment variables:
   ```bash
   vercel env add VITE_FIREBASE_API_KEY
   vercel env add VITE_FIREBASE_AUTH_DOMAIN
   vercel env add VITE_FIREBASE_PROJECT_ID
   vercel env add VITE_FIREBASE_STORAGE_BUCKET
   vercel env add VITE_FIREBASE_MESSAGING_SENDER_ID
   vercel env add VITE_FIREBASE_APP_ID
   vercel env add VITE_API_BASE_URL
   ```
   
   Enter the values when prompted.

6. Redeploy to apply environment variables:
   ```bash
   vercel --prod
   ```

#### Option B: Using Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your Git repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend` (if your frontend is in a subdirectory)
   - **Build Command**: `npm run build` (or `yarn build`)
   - **Output Directory**: `dist`
   - **Install Command**: `npm install` (or `yarn install`)

5. Add Environment Variables:
   - Click **"Environment Variables"**
   - Add each variable:
     - `VITE_FIREBASE_API_KEY`
     - `VITE_FIREBASE_AUTH_DOMAIN`
     - `VITE_FIREBASE_PROJECT_ID`
     - `VITE_FIREBASE_STORAGE_BUCKET`
     - `VITE_FIREBASE_MESSAGING_SENDER_ID`
     - `VITE_FIREBASE_APP_ID`
     - `VITE_FIREBASE_VAPID_KEY` (optional, for notifications)
     - `VITE_API_BASE_URL` = `https://your-service-name.onrender.com/api`

6. Click **"Deploy"**

### Step 3: Update Backend CORS

After deploying to Vercel, you'll get a URL like: `https://your-project.vercel.app`

1. Go to Render Dashboard → Your Backend Service → Environment
2. Update CORS configuration in `backend_python/app/main.py`:
   ```python
   # Replace <MY_VERCEL_DOMAIN> with your actual Vercel domain
   CORS_ORIGIN_REGEX = r"https://.*\.vercel\.app|https://your-project.vercel.app|http://localhost:5173"
   ```
   
   Or add it as an environment variable and read it in the code.

3. Redeploy the backend (Render will auto-deploy on git push, or click "Manual Deploy")

### Step 4: Verify Frontend

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Try logging in with Firebase Auth
3. Test API calls to ensure they work

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend returns 401 Unauthorized
- **Solution**: Check that `serviceAccountKey.json` is correctly uploaded in Render Secret Files
- Verify `FIREBASE_CREDENTIALS_PATH` points to the correct file path

**Problem**: Backend fails to start
- **Solution**: Check Render logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` includes all dependencies

**Problem**: CORS errors in browser
- **Solution**: Verify CORS regex includes your Vercel domain
- Check that `allow_credentials=True` is set

### Frontend Issues

**Problem**: Environment variables not working
- **Solution**: Vite requires `VITE_` prefix for all environment variables
- Redeploy after adding environment variables
- Check Vercel build logs for errors

**Problem**: API calls fail with 401
- **Solution**: Verify `VITE_API_BASE_URL` is correct
- Check that Firebase Auth is initialized
- Verify token is being sent in Authorization header

**Problem**: Firebase initialization fails
- **Solution**: Check all `VITE_FIREBASE_*` environment variables are set
- Verify Firebase project settings match

---

## 📝 Environment Variables Summary

### Backend (Render)

```bash
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CREDENTIALS_PATH=/opt/render/project/src/serviceAccountKey.json
DEBUG=False
PORT=10000  # Auto-set by Render
```

### Frontend (Vercel)

```bash
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_FIREBASE_VAPID_KEY=your-vapid-key  # Optional
VITE_API_BASE_URL=https://your-service-name.onrender.com/api
```

---

## 🔐 Security Checklist

- [ ] `serviceAccountKey.json` is NOT committed to Git
- [ ] `.gitignore` includes `serviceAccountKey.json`
- [ ] All sensitive keys are in environment variables
- [ ] CORS is configured to only allow your frontend domain
- [ ] Backend requires authentication for protected endpoints
- [ ] Firebase Security Rules are configured for Firestore

---

## 🎉 Success!

Once deployed, your application should be:
- ✅ Backend running on Render
- ✅ Frontend running on Vercel
- ✅ Firebase Authentication working
- ✅ API calls authenticated with Firebase tokens
- ✅ CORS configured correctly

**Next Steps:**
- Set up custom domains (optional)
- Configure Firebase Security Rules
- Set up monitoring and logging
- Enable HTTPS (automatic on Render/Vercel)

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

