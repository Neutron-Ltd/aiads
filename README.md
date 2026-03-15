# Ads Co-Pilot

Human-in-the-loop AI web application for managing and creating Google Ads campaigns.

## Tech Stack

- **Frontend:** Next.js (React), Tailwind CSS, Shadcn UI, Recharts
- **Backend:** Python 3.11+, FastAPI
- **AI:** Google Gemini API
- **Ads:** Google Ads API (production-ready, real data)

## Project Structure

```
aiads/
├── frontend/           # Next.js app
├── backend/            # FastAPI app
│   └── ads_copilot.db  # SQLite (dev) or use PostgreSQL in production
└── README.md
```

## Setup

### Prerequisites

- Node.js 18+
- Python 3.11+ (use `python3` if `python` is not available)
- npm or pnpm

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the environment template and configure:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the environment template (optional for local dev):
   ```bash
   cp .env.local.example .env.local
   # Set NEXT_PUBLIC_API_URL if your backend runs elsewhere
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:3000`.

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API key for Gemini. Get from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |

### Google Ads API (required for production)

| Variable | Description |
|----------|-------------|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | From [Google Ads API Center](https://ads.google.com/aw/apicenter) |
| `GOOGLE_ADS_CLIENT_ID` | OAuth 2.0 client ID (Google Cloud Console) |
| `GOOGLE_ADS_CLIENT_SECRET` | OAuth 2.0 client secret |
| `GOOGLE_ADS_REFRESH_TOKEN` | Obtained after user OAuth flow ([generate_user_credentials.py](https://developers.google.com/google-ads/api/docs/client-libs/python/oauth-web)) |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | Optional. MCC account ID for manager accounts (format: 123-456-7890) |

### Production

| Variable | Description |
|----------|-------------|
| `ENVIRONMENT` | `production` for production mode |
| `DATABASE_URL` | PostgreSQL connection string, e.g. `postgresql://user:pass@host:5432/ads_copilot` |
| `CORS_ORIGINS` | Comma-separated allowed origins, e.g. `https://app.example.com` |

## Production Deployment

1. **Database:** Use PostgreSQL. Set `DATABASE_URL` in your environment.
2. **Google Ads:** Configure all `GOOGLE_ADS_*` variables. Use a service account or OAuth flow to obtain a refresh token.
3. **CORS:** Set `CORS_ORIGINS` to your frontend domain(s).
4. **Environment:** Set `ENVIRONMENT=production`.
5. **Projects:** When creating a project, set `google_ads_customer_id` to link it to a Google Ads account (format: 123-456-7890).

## Routes

| Route                | Path                  |
|----------------------|-----------------------|
| Projects             | `/projects`           |
| Dashboard            | `/`                   |
| Keyword Sandbox      | `/keyword-sandbox`    |
| Creative Studio      | `/creative-studio`    |
| Campaign Architect   | `/campaign-architect` |
| Optimization Inbox   | `/optimization-inbox` |

On first visit, you will be redirected to the Project Manager (`/projects`) to select or create a project before accessing the Dashboard.

## Development

- **Frontend:** `cd frontend && npm run dev`
- **Backend:** `cd backend && uvicorn app.main:app --reload`

Run both in separate terminals for full-stack development.
