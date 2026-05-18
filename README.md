# Ifugao PPO BMI Monitoring App

This workspace contains a full-stack BMI monitoring system for Ifugao PPO personnel.

## Structure

- `backend/` - Django REST API and data models
- `frontend/` - React + Vite app for personnel and admin interfaces

## Backend Setup

1. Open a terminal in `backend/`
2. Create and activate a virtual environment:
   - Windows PowerShell:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
3. Upgrade pip and install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements-dev.txt
   ```
4. Create database tables:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the Django server:
   ```powershell
   python manage.py runserver
   ```

The API is available at `http://localhost:8000/api/`.

> Note: `requirements-dev.txt` is recommended for local Windows development. `requirements.txt` includes `gunicorn` and is intended for deployment in Docker or Linux environments.

### Default Admin Account

- Username: `ifugao_admin`
- Password: `Admin1234`

After the first admin login, the app requires a password change.

## Frontend Setup

1. Install Node.js and npm if you do not already have them installed.
   - Download from https://nodejs.org/
2. Open a terminal in `frontend/`
3. Install dependencies:
   ```powershell
   npm install
   ```
4. Start the development server:
   ```powershell
   npm run dev
   ```

The frontend will typically run at `http://localhost:5173`.

## Features

- Personnel signup with rank, name, birthdate, unit, username, and password validation
- Personnel login and BMI computation dashboard
- Age calculation based on birthdate, updated dynamically
- BMI results with PNP and WHO classification
- Weight-to-lose and maximum normal weight calculations
- Admin login with first-login password change and forgot-password QR code flow
- Admin dashboard with full personnel list, edit/delete actions, and Excel export

## Notes

- The backend uses SQLite for ease of setup.
- CORS is enabled for `http://localhost:5173`.

## Render Deployment

This repo includes `render.yaml` for Render deployment. It currently defines the backend service only.

- `Ifugao BMI Backend` as a Docker web service using `backend/Dockerfile`

### Frontend deployment on Render

The frontend must be deployed separately as a Render Static Site.

### Render Environment Variables

- `VITE_API_URL` (frontend): set to `https://YOUR_BACKEND_SERVICE.onrender.com/api`
- `DJANGO_SETTINGS_MODULE` (backend): `bmi_monitor.settings`

### Deploy steps on Render

1. Deploy the backend service from `render.yaml`.
2. Create a Render Static Site for the frontend using the same repo.
3. In the frontend service settings, set `VITE_API_URL` to the backend service URL + `/api`.
4. Deploy the frontend as a separate static site.

> Note: The Render blueprint only supports the backend service; the frontend is deployed manually as a static site.

## Local Docker Compose

To run both services locally with Docker Compose:

```bash
docker-compose up --build
```

- Backend will be available at `http://localhost:8000`
- Frontend will be available at `http://localhost:5173`

The frontend build uses `VITE_API_URL=http://backend:8000/api` in local compose setup.
