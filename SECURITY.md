# Security Policy

## Reporting a vulnerability

Please report security issues privately by email to **info@neutron.com.bd**.
Do not open a public GitHub issue for a vulnerability.

Include as much of the following as you can:

- a description of the issue and its impact
- steps to reproduce, or a proof of concept
- the affected version or commit

We aim to acknowledge reports within 5 business days and will keep you updated
while we work on a fix. Please give us reasonable time to release a fix before
disclosing the issue publicly.

## Supported versions

Only the latest commit on `main` receives security fixes.

## Deployment notes

- The API has **no built-in authentication**. Do not expose the backend to the
  public internet without putting it behind your own authentication layer
  (reverse proxy, VPN, SSO gateway, etc.).
- Keep all credentials in environment variables or a secrets manager. Never
  commit `.env` files, `google-ads.yaml`, OAuth client JSON files or refresh
  tokens.
- Set `ENVIRONMENT=production` in production; this disables the interactive
  API docs.
- Set `CORS_ORIGINS` to the exact origin(s) of your frontend. Wildcards are
  rejected.
