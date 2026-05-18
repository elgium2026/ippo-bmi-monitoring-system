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
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
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

### Default Admin Account

- Username: `ifugao_admin`
- Password: `Admin1234`

After the first admin login, the app requires a password change.

## Frontend Setup

1. Open a terminal in `frontend/`
2. Install dependencies:
   ```powershell
   npm install
   ```
3. Start the development server:
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

This repo includes `render.yaml` for Render deployment. It defines two services:

- `Ifugao BMI Backend` as a Python web service using `backend/`
- `Ifugao BMI Frontend` as a static site using `frontend/`

### Render Environment Variables

- `VITE_API_URL` (frontend): set to `https://YOUR_BACKEND_SERVICE.onrender.com/api`
- `DJANGO_SETTINGS_MODULE` (backend): `bmi_monitor.settings`

### Deploy steps on Render

1. Create a new Render service for the backend using the repo and Python environment.
2. Create a second Render service for the frontend as a static site.
3. In the frontend service settings, set `VITE_API_URL` to the backend service URL + `/api`.
4. Deploy both services.

## Local Docker Compose

To run both services locally with Docker Compose:

```bash
docker-compose up --build
```

- Backend will be available at `http://localhost:8000`
- Frontend will be available at `http://localhost:5173`

The frontend build uses `VITE_API_URL=http://backend:8000/api` in local compose setup.
