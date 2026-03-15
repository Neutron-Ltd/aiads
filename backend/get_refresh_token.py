#!/usr/bin/env python3
"""
Temporary script to obtain a Google Ads OAuth2 refresh token via the Desktop App flow.
Run once, then add GOOGLE_ADS_REFRESH_TOKEN to your backend/.env file.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load .env from the backend directory (where this script lives)
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)

SCOPE = "https://www.googleapis.com/auth/adwords"
# Fixed port so redirect URI matches Google Cloud Console (add this exact URI there)
LOCAL_PORT = 8080
REDIRECT_URI = f"http://localhost:{LOCAL_PORT}/"

client_config = {
    "installed": {
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI, "http://127.0.0.1:{}/".format(LOCAL_PORT)],
    }
}


def main():
    client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    if not client_id or not client_secret:
        print("Error: GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET must be set in backend/.env")
        return

    print("If you get 'redirect_uri_mismatch', add this to your OAuth client in Google Cloud Console:")
    print("  Authorized redirect URIs: " + REDIRECT_URI)
    print()

    flow = InstalledAppFlow.from_client_config(client_config, scopes=[SCOPE])
    credentials = flow.run_local_server(port=LOCAL_PORT)

    refresh_token = credentials.refresh_token
    print()
    print("=" * 60)
    print("SUCCESS — Copy this refresh token into backend/.env")
    print("=" * 60)
    print()
    print("GOOGLE_ADS_REFRESH_TOKEN=" + refresh_token)
    print()
    print("Add or update the line above in backend/.env, then delete this script if desired.")
    print("=" * 60)


if __name__ == "__main__":
    main()
