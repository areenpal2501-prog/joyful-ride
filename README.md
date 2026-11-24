# JoyRide

JoyRide is an Expo app with a FastAPI backend. For local development, the
backend uses an in-memory store by default, so you can run the complete ride
flow without setting up MongoDB. Bookings reset whenever the backend restarts.

## Prerequisites

- Node.js 20 or newer with Corepack enabled
- Python 3.10 or newer

## First-time setup (Windows PowerShell)

In the project folder, install the frontend dependencies:

```powershell
cd frontend
corepack yarn install
```

In a second PowerShell window, install and start the backend:

```powershell
cd backend
$python = Get-ChildItem "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe" | Select-Object -First 1 -ExpandProperty FullName
& $python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn server:app --host 0.0.0.0 --port 8002 --reload
```

Then start the app in a third window:

```powershell
cd frontend
corepack yarn web
```

Open the local URL printed by Expo. The frontend calls `http://localhost:8002`
for the API. Keep the backend terminal open while using the app.

## Expo Go on a phone

The default backend URL is for a browser on the same computer. To use Expo Go,
change `EXPO_PUBLIC_BACKEND_URL` in `frontend/.env` to the computer's LAN URL,
for example `http://192.168.1.20:8002`. Keep both devices on the same network,
allow the backend through the computer's firewall, and restart Expo after
changing `.env`.

## Persistent storage

The local default stores bookings in memory. To persist them in MongoDB, set
`DATABASE_MODE=mongo`, `MONGO_URL`, and `DB_NAME` in `backend/.env` and start
MongoDB before the API. Dependency pins for the backend are in
`backend/requirements.txt`.
