"""Authentik OAuth2 authentication."""
from fastapi import HTTPException, Request
from httpx import AsyncClient

from .config import settings


async def get_authentik_user(request: Request) -> dict:
    """Validate session and return user info from Authentik.

    Usage:
        @app.get("/protected")
        async def protected(user: dict = Depends(get_authentik_user)):
            return {"user": user["preferred_username"]}
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if not settings.authentik_domain:
        raise HTTPException(status_code=500, detail="Authentik not configured")

    async with AsyncClient() as client:
        resp = await client.get(
            f"https://{settings.authentik_domain}/application/o/userinfo/",
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        return resp.json()


# OAuth2 login/callback routes - add to main.py if using Authentik
"""
from fastapi import APIRouter
from fastapi.responses import RedirectResponse

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/login")
async def login():
    auth_url = (
        f"https://{settings.authentik_domain}/application/o/authorize/"
        f"?client_id={settings.authentik_client_id}"
        f"&redirect_uri=https://myapp.{settings.domain_base}/auth/callback"
        f"&response_type=code"
        f"&scope=openid%20profile%20email"
    )
    return RedirectResponse(auth_url)

@auth_router.get("/callback")
async def callback(code: str):
    # Exchange code for token, set cookie, redirect to app
    ...
"""
