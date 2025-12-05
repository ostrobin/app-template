# Project: app-template

Reference: /srv/INSTANCE.md for shared services

## Stack
- FastAPI + Uvicorn, SQLAlchemy 2.0 async + asyncpg
- Pydantic 2.5+, httpx, Jinja2 + HTMX (UI optional)

## Code Quality
- Black (formatter), Ruff (linter), config in pyproject.toml

## Scalability Principles - ENFORCED BY PRE-COMMIT HOOK

**Pre-commit hook validates (.git/hooks/pre-commit):**
- CSS ≤ 150 lines
- No hex colors outside `:root`
- No `if slug == "x"` patterns in services

**BEFORE writing code, ask:**
1. "Does this work for N contexts/items without code changes?"
2. "All colors in `:root`, all spacing in CSS variables?"
3. "Am I copy-pasting? → Extract to shared function"

| ❌ WRONG | ✅ RIGHT |
|----------|----------|
| `color: #8ab4f8;` | `color: var(--accent);` |
| `.save-btn { padding: 8px 16px; }` | `button { padding: 8px 16px; }` |
| `if context.slug == "foo":` | Generic JSONB handler |
| Copy-paste validation | `from app.utils import validate` |

## CSS/Frontend
- Colors ONLY in `:root` block (exception: `#000`, `#fff`)
- Style base elements (`button`, `input`, `select`) globally
- Utility classes (`.card`, `.label`, `.tag`) over component-specific
- Max 150 lines - refactor if approaching limit

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
- Check /srv/ports.env for next available port (see "# Next:" line)
- Port ranges: 81xx for apps (8100, 8110, 8120...)
- Update docker-compose.yml healthcheck with your port BEFORE running sync script
- Run: /srv/scripts/sync-ports.sh

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
