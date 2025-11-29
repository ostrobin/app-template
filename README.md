# App Template

Template for new FastAPI apps. See CLAUDE.md for conventions.

## Deployment

1. Copy: `cp -r app-template apps/myapp`
2. Rename in docker-compose.yml, Dockerfile
3. Add port to /srv/ports.env: `MYAPP_PORT=8xxx`
4. Run: `/srv/scripts/sync-ports.sh`
5. Add to /srv/.env: MYAPP_DATABASE_URL, MYAPP_* vars
6. Add Caddyfile entry for myapp.{DOMAIN_BASE}
7. Create DB and add to PgBouncer:
   ```bash
   docker exec postgres psql -U postgres -c "CREATE DATABASE myapp;"
   docker exec postgres psql -U postgres -c "CREATE USER myapp WITH PASSWORD 'xxx';"
   docker exec postgres psql -U postgres -c "GRANT ALL ON DATABASE myapp TO myapp;"
   # Add to /srv/data/pgbouncer/userlist.txt: "myapp" "xxx"
   # Add to /srv/data/pgbouncer/pgbouncer.ini [databases]: myapp = host=postgres dbname=myapp
   docker restart pgbouncer
   ```
   Note: DATABASE_URL should use pgbouncer:5432 (internal), not postgres:5432
8. Deploy: `cd apps/myapp && set -a && source ../../.env && set +a && docker compose up -d`
9. TLS: `docker restart caddy`

## Authentik SSO Setup

1. Authentik Admin → Applications → Providers → Create OAuth2
2. Client ID: myapp, generate secret
3. Redirect URI: https://myapp.{DOMAIN_BASE}/auth/callback
4. Add to .env: MYAPP_AUTHENTIK_CLIENT_ID, MYAPP_AUTHENTIK_CLIENT_SECRET
5. Restart app
