# NgombeBora

NgombeBora is a single-farm cow inventory and farm management app. The backend is a Flask JSON API backed by Flask-SQLAlchemy; the frontend is a React single-page app built with Vite.

## Folder structure

- `backend/app.py` — SQLAlchemy models, automatic cow serial assignment, validation, and API routes for cows, milk records, finance, and dashboard summaries. The app factory creates the tables on startup.
- `backend/config.py` — environment-based database configuration. PostgreSQL is used when `DATABASE_URL` is set; SQLite is the local fallback.
- `backend/requirements.txt` — Python dependencies.
- `frontend/src/main.jsx` — React navigation, dashboard, registration forms, milk log, and finance ledger.
- `frontend/src/styles.css` — responsive application styling.
- `frontend/index.html`, `frontend/vite.config.js`, `frontend/package.json` — Vite entry point and frontend scripts.

## Run locally

Set `DATABASE_URL` to a PostgreSQL connection string in `backend/.env` (for example `postgresql://localhost/ngombebora`), then start the API:

```sh
cd backend
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python app.py
```

In another terminal:

```sh
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://localhost:5000/api`. Set `VITE_API_URL` to override it. CORS is enabled for the API.

## API overview

- `GET /api/dashboard`
- `GET /api/cows`; `POST /api/cows/purchased`; `POST /api/cows/newborn`; `PATCH /api/cows/:id/status`
- `GET /api/milk`; `POST /api/milk`
- `GET /api/finance`; `POST /api/finance`; `GET /api/finance/categories`

Finance filters accept `start`, `end`, and `type` query parameters. Amounts and quantities are returned as JSON numbers. Cow serial numbers are assigned by the server and are not accepted from the client.
