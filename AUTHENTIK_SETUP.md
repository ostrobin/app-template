# Authentik SSO Setup Guide

Step-by-step guide to configure Authentik OAuth2 for a new app.

## Prerequisites

- Authentik running at `auth.{DOMAIN_BASE}`
- App deployed with auth routes (see `app/auth.py`)
- Admin access to Authentik

-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------

## MANUAL STEPS (User does these in Authentik UI)

### Step 1: Create OAuth2 Provider

1. Go to **https://auth.{DOMAIN_BASE}**
2. Login as admin
3. Navigate to **Admin Interface** → **Applications** → **Providers**
4. Click **Create**
5. Select **OAuth2/OpenID Provider**
6. Fill in:
   - **Name**: `myapp` (lowercase, no spaces)
   - **Authentication flow**: `default-authentication-flow (Welcome to authentik!)`
   - **Authorization flow**: `default-provider-authorization-implicit-consent` or `explicit-consent`
7. Expand **Protocol settings**:
   - **Client type**: `Confidential`
   - **Redirect URIs**: `https://myapp.{DOMAIN_BASE}/auth/callback`
8. Click **Finish**

### Step 2: Create Application

1. Navigate to **Admin Interface** → **Applications** → **Applications**
2. Click **Create**
3. Fill in:
   - **Slug**: `myapp`
   - **Provider**: Select `myapp` (the provider you just created)
   - **Policy engine mode**: `any`
4. Click **Create**

### Step 3: Get Client Credentials

1. Go back to **Providers** → click on **myapp**
2. Copy these values:
   - **Client ID** (e.g., `Y7tUgsdsd04aNyzOjXNaIgkU1zxyz`)
   - **Client Secret** (click eye icon to reveal, e.g., `hRUqKwMJGyiO...`)

-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------

## AUTOMATED STEPS (Claude/script does these)

### Step 4: Configure App Environment

Add to `/srv/.env`:

```bash
# Authentik SSO for MyApp
MYAPP_AUTHENTIK_CLIENT_ID=<paste Client ID>
MYAPP_AUTHENTIK_CLIENT_SECRET=<paste Client Secret>

# These should already exist (shared):
# AUTHENTIK_DOMAIN=auth.{DOMAIN_BASE}
# DOMAIN_BASE={your domain}
```

If `AUTHENTIK_DOMAIN` doesn't exist, add it:
```bash
AUTHENTIK_DOMAIN=auth.soljudigital.fi
```

### Step 5: Restart App

```bash
cd /srv/apps/myapp
set -a && source /srv/.env && set +a && docker compose up -d --force-recreate
```

Verify env vars loaded:
```bash
docker exec myapp env | grep AUTHENTIK
```

Should show:
```
AUTHENTIK_CLIENT_ID=Y7tUgkkRDR04aNyz...
AUTHENTIK_CLIENT_SECRET=hRUqKwMJGyiO...
AUTHENTIK_DOMAIN=auth.soljudigital.fi
```

### Step 6: Test

1. Go to `https://myapp.{DOMAIN_BASE}/ui/login`
2. You should see **"Sign in with SSO"** button
3. Click it → redirects to Authentik login
4. After login → redirects back to app, logged in

## Troubleshooting

### "SSO not configured" error
- Check env vars are set in container: `docker exec myapp env | grep AUTHENTIK`
- Restart with `set -a && source /srv/.env && set +a` before docker compose

### "invalid_state" error
- State cookie expired (>10 min) - try again
- Cookies blocked - check browser settings

### "token_failed" error
- Wrong Client Secret - verify in Authentik provider settings
- Wrong redirect URI - must match exactly: `https://myapp.{DOMAIN_BASE}/auth/callback`

### 404 on /auth/callback
- App not rebuilt with auth routes
- Run: `docker compose up -d --build`

### Provider not assigned warning
- Go to Applications, ensure the application is linked to the provider
