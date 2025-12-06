# Deployment Guide for Render

## Quick Setup

1. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Select "Python" as the environment

2. **Configure Build & Start Commands**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `DATABASE_URL`: Your PostgreSQL connection string (e.g., `postgresql://user:password@host:5432/dbname`)
   - `SECRET_KEY`: A secure random string (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
   - `DEBUG`: `False` (for production)
   - `PORT`: `5000` (Render sets this automatically via `$PORT`)

4. **Database Setup**
   - Create a PostgreSQL database on Render or use Google Cloud SQL
   - The app will automatically create tables on first startup via `init_db()`
   - For migrations, you can run: `alembic upgrade head` (if needed)

## Important Notes

- **This is a FastAPI application, NOT Django**
- Render will automatically detect Python and use the start command from `render.yaml` or `Procfile`
- The `DATABASE_URL` should be in format: `postgresql://user:password@host:port/dbname`
- The app converts it to `postgresql+asyncpg://` automatically for async operations

## Troubleshooting

If Render tries to run Django commands:
1. Ensure there's no `manage.py` or `wsgi.py` in the root
2. Check that `render.yaml` specifies the correct start command
3. Verify `Procfile` exists with: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`

