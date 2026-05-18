# Render Deployment Changes Summary

## Files Modified

### 1. **render.yaml** (Complete rewrite)
   - Added Frontend service (React/Nginx) on separate URL
   - Added PostgreSQL database service (`ifugao-bmi-db`)
   - Backend now includes:
     - `startCommand` with migrations and collectstatic
     - Health check path
     - Environment variables for production
   - Frontend uses `fromService` reference to automatically link to backend URL
   - All services set to `plan: free` for Render's free tier

### 2. **backend/bmi_monitor/settings.py**
   - **SECRET_KEY**: Now read from `SECRET_KEY` env var (Render auto-generates)
   - **DEBUG**: Now controlled by `DEBUG` env var (set to `False` in production)
   - **ALLOWED_HOSTS**: Dynamically built from `ALLOWED_HOSTS` env var
   - **DATABASES**: 
     - Uses SQLite locally (default)
     - Switches to PostgreSQL when `DATABASE_URL` env var is present
   - **MIDDLEWARE**: Added `whitenoise.middleware.WhiteNoiseMiddleware` for static file serving
   - **STATIC_ROOT**: Added for production static file handling
   - **STATICFILES_STORAGE**: Using WhiteNoise's compressed manifest storage
   - **CORS_ALLOWED_ORIGINS**: Dynamically from env var (supports comma-separated list)
   - **Security settings**: Added HTTPS redirect, secure cookies, and CSP headers for production

### 3. **backend/requirements.txt**
   - ✅ Added `whitenoise==6.6.0` - for serving static files in production
   - ✅ Added `dj-database-url==2.1.0` - for parsing DATABASE_URL
   - ✅ Added `psycopg2-binary==2.9.9` - PostgreSQL driver for Django

### 4. **frontend/Dockerfile**
   - Added `ARG VITE_API_URL` build argument
   - Frontend build now accepts API URL from Render (defaults to localhost:8000 for local dev)
   - Added `nginx.conf` copy for production Nginx configuration
   - Nginx configured with proper caching, gzip, and SPA routing

### 5. **frontend/nginx.conf** (New file)
   - ✅ Gzip compression enabled
   - ✅ Smart caching for assets (30 days) vs HTML (1 day)
   - ✅ Client-side routing support (all non-file requests → index.html)
   - ✅ Optional API proxy (commented out, can be enabled if needed)

### 6. **backend/.env.example** (New file)
   - Environment variable reference for backend deployment
   - Includes all configuration options with descriptions

### 7. **frontend/.env.example** (New file)
   - Environment variable reference for frontend deployment
   - Shows how VITE_API_URL is used

### 8. **DEPLOYMENT.md** (New file)
   - Comprehensive deployment guide
   - Local development setup
   - Step-by-step Render deployment
   - Admin account creation instructions
   - Troubleshooting guide
   - Monitoring and backup strategies

## How Render Deployment Works

1. **Repository**: Push code to Git (GitHub/GitLab/Bitbucket)
2. **Blueprint**: Use `render.yaml` as infrastructure-as-code
3. **Services created**:
   - Frontend: React SPA served by Nginx (~5-10 min build)
   - Backend: Django API with Gunicorn (~3-5 min build)
   - Database: PostgreSQL (auto-provisioned)
4. **Environment Variables**: 
   - Render generates `SECRET_KEY` automatically
   - `DATABASE_URL` is auto-set from postgres service
   - Frontend `VITE_API_URL` is auto-populated from backend service URL

## Pre-Deployment Checklist

- [ ] Code pushed to Git repository (main branch)
- [ ] All files above are in place
- [ ] `requirements.txt` has all dependencies
- [ ] `render.yaml` is in repository root
- [ ] Frontend and backend Dockerfiles are present
- [ ] No hardcoded database URLs or secrets in code

## Local Testing (Before Deployment)

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm install
VITE_API_URL=http://localhost:8000/api npm run dev
```

Visit: `http://localhost:5173` → backend at `http://localhost:8000`

## Deployment Steps

1. Push to Git: `git push origin main`
2. Go to Render.com → New Blueprint
3. Connect Git repository
4. Select `main` branch
5. Review `render.yaml` services
6. Click "Deploy"
7. Wait ~15-20 minutes for both services to build and start
8. Visit frontend URL and test signup/login/dashboard

## After Deployment

1. Create admin account (see DEPLOYMENT.md)
2. Verify backend health: `GET https://<backend>/api/admin/login/`
3. Test frontend: Sign up, login, compute BMI
4. Test admin login with Google Authenticator
5. Test export to Excel

## Key Architecture

```
┌─────────────────────┐
│  Browser/User      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────┐
│  Render Frontend            │ ◄─ Nginx on :80/443
│  (React SPA)                │    Static files, SPA routing
│  https://...onrender.com    │
└──────────┬──────────────────┘
           │
           │ CORS-enabled
           │ /api calls
           ▼
┌──────────────────────────────┐
│  Render Backend              │ ◄─ Gunicorn on :8000
│  (Django REST API)           │    JWT auth, BMI logic
│  https://...onrender.com     │    Admin/Personnel endpoints
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Render PostgreSQL Database  │
│  (ifugao_bmi_prod)           │
└──────────────────────────────┘
```

---

## Questions or Issues?

- Check DEPLOYMENT.md for detailed troubleshooting
- Review Render service logs in Dashboard
- Verify environment variables are set correctly
- Ensure frontend/backend Dockerfiles build locally first

Deployment is ready! 🚀
