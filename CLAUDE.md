# Project: app-template

Reference: /srv/INSTANCE.md for shared services

## Stack
- FastAPI + Uvicorn, SQLAlchemy 2.0 async + asyncpg
- Pydantic 2.5+, httpx, Jinja2 + HTMX (UI optional)

## Code Quality
- Black (formatter), Ruff (linter), config in pyproject.toml

## Scalability Principles (ALL code)
- No hardcoded values: use variables/constants/config for anything reused
- No one-off solutions; prefer reusable patterns
- Keep files small: CSS ~150 lines, Python modules focused and single-purpose
- DRY: extract common logic to shared utilities; copy-paste is a red flag
- **STRICT: Any deviation from these principles requires explicit user approval**

Examples:
| ❌ WRONG | ✅ RIGHT |
|----------|----------|
| `color: #8ab4f8;` | `color: var(--accent);` |
| `.save-btn { padding: 8px 16px; }` | `button { padding: 8px 16px; }` |
| Copy-pasting 10 lines of validation | `from app.utils import validate_input`

## CSS/Frontend
- Use CSS variables (`:root`) for colors/spacing/sizing
- Style base elements (button, input) globally, not per-component
- Prefer inheritance over component-specific classes

## Development Workflow
1. Backend first: routes, services, models
2. Health endpoint: GET /health returns {"status": "ok"}
3. API working and tested before any UI
4. UI last: templates + HTMX on top of working API

## API Conventions
- GET /health, GET /items, GET /items/{id}
- POST /items, PUT /items/{id}, DELETE /items/{id}
- All return JSON, UI uses same endpoints

## Auth (Authentik SSO - Preferred)
- Env: AUTHENTIK_CLIENT_ID, AUTHENTIK_CLIENT_SECRET, AUTHENTIK_DOMAIN
- Redirect: https://{app}.{DOMAIN_BASE}/auth/callback
- See: app/auth.py

## Auth Alternatives
- HTTP Basic: middleware, BASIC_AUTH_* env vars
- API Key: X-API-Key header, user.api_key in DB

## Ports
- Update /srv/ports.env, run /srv/scripts/sync-ports.sh
- Convention: xx00=API, xx01=UI

## Database
- Connection: pgbouncer:5432
- Pattern: Route → Service → ORM (no SQL in routes)
- Migrations: Alembic (alembic revision --autogenerate, alembic upgrade head)

## Logging
- Format: JSON to stdout
- Level: INFO default

## Errors
- HTTPException for 4xx client errors
- Log and raise for 5xx server errors
- No bare except clauses

## Testing
- pytest + pytest-asyncio, httpx.AsyncClient

## Docker
- Base: python:3.11-slim
- Networks: public_proxy, private
- Healthcheck: GET /health

## Rules
- Config via env only, no secrets in git
- Logs to stdout, stateless (data in Postgres)
