# Ads Co-Pilot

A human-in-the-loop web app for planning and managing Google Ads campaigns.
You organise work into **projects**. Each project links to a Google Ads account,
and the backend can pull live campaign metrics and search-term reports from the
Google Ads API.

> **Status:** early stage. Project management and the Google Ads data service
> work today. The Keyword Sandbox, Creative Studio, Campaign Architect and
> Optimization Inbox pages are placeholders for upcoming AI-assisted features.

## Tech stack

| Layer    | Technology                                             |
|----------|--------------------------------------------------------|
| Frontend | Next.js 16 (React 19), Tailwind CSS 4, shadcn/ui        |
| Backend  | Python 3.10+, FastAPI, SQLModel                        |
| Database | SQLite for development, PostgreSQL for production      |
| Ads      | Google Ads API (`google-ads` client library)           |

## Project structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/routes/   # REST endpoints (/api/v1/projects)
│   │   ├── models/          # SQLModel tables
│   │   ├── schemas/         # Request/response models
│   │   ├── services/        # Google Ads integration
│   │   ├── config.py        # Settings loaded from environment variables
│   │   └── main.py          # FastAPI app
│   ├── get_refresh_token.py # One-off helper to obtain a Google Ads refresh token
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # Next.js app
│   └── .env.local.example
├── .env.example             # Overview of every setting
├── LICENSE
└── SECURITY.md
```

## Getting started

### Prerequisites

- Node.js 20+ and npm
- Python 3.10+

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then edit .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Interactive docs are at `/docs` when
`ENVIRONMENT` is not `production`.

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local   # set NEXT_PUBLIC_API_URL if needed
npm run dev
```

The app runs at `http://localhost:3000`. On first visit you are sent to
`/projects` to create or select a project.

## Configuration

All configuration comes from environment variables. The backend reads them from
`backend/.env`, and the frontend from `frontend/.env.local`. The repository has
no default credentials.

### Backend

| Variable                       | Required | Description |
|--------------------------------|----------|-------------|
| `ENVIRONMENT`                  | no       | `development` (default) or `production`. Production disables the API docs. |
| `DEBUG`                        | no       | `true` to log SQL statements. |
| `DATABASE_URL`                 | no       | Defaults to `sqlite:///./ads_copilot.db`. Use a PostgreSQL URL in production. |
| `CORS_ORIGINS`                 | no       | Comma-separated exact frontend origins. Defaults to `http://localhost:3000`. `*` is rejected. |
| `GOOGLE_ADS_DEVELOPER_TOKEN`   | for live data | From the [Google Ads API Center](https://ads.google.com/aw/apicenter). |
| `GOOGLE_ADS_CLIENT_ID`         | for live data | OAuth 2.0 client ID (Google Cloud Console). |
| `GOOGLE_ADS_CLIENT_SECRET`     | for live data | OAuth 2.0 client secret. |
| `GOOGLE_ADS_REFRESH_TOKEN`     | for live data | Generate with `python get_refresh_token.py`. |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | no       | Manager (MCC) account ID, if you access client accounts through one. |
| `GEMINI_API_KEY`               | no       | Reserved for upcoming AI features. Not used yet. |
| `OAUTH_REDIRECT_PORT`          | no       | Local port for `get_refresh_token.py` (default `8080`). |

### Frontend

| Variable              | Description |
|-----------------------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend base URL. Defaults to `http://localhost:8000`. |

### Getting a Google Ads refresh token

1. In Google Cloud Console, create an OAuth client of type **Desktop app**. Add
   `http://localhost:8080/` as an authorized redirect URI, or use the port you set
   in `OAUTH_REDIRECT_PORT`.
2. Put `GOOGLE_ADS_CLIENT_ID` and `GOOGLE_ADS_CLIENT_SECRET` in `backend/.env`.
3. Run `python get_refresh_token.py` from `backend/`, sign in, and copy the
   printed `GOOGLE_ADS_REFRESH_TOKEN` into `backend/.env`.

## API

| Method | Path                           | Description |
|--------|--------------------------------|-------------|
| GET    | `/health`                      | Health check |
| GET    | `/api/v1/projects`             | List projects |
| POST   | `/api/v1/projects`             | Create a project |
| GET    | `/api/v1/projects/{id}`        | Get a project |
| GET    | `/api/v1/projects/{id}/full`   | Get a project with its campaigns, keywords and ad copy |
| PUT    | `/api/v1/projects/{id}`        | Update a project |
| DELETE | `/api/v1/projects/{id}`        | Delete a project |

## Production notes

- Use PostgreSQL. Set `DATABASE_URL`, `ENVIRONMENT=production` and `CORS_ORIGINS`.
- The API has **no built-in authentication**. Run it behind your own auth layer,
  such as a reverse proxy, VPN or SSO gateway. Do not expose it publicly as-is.
- Store credentials in your platform's secret store, not in files.

## Security

See [SECURITY.md](SECURITY.md) for how to report a vulnerability.

## License

[MIT](LICENSE) © Shamir Shakher, Neutron Ltd
