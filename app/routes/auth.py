import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from app.utils import email_imap

router = APIRouter()

# OAuth Setup
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"response_type": "code", "scope": "https://mail.google.com/"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "https://mail.google.com/"},
)

oauth.register(
    name="microsoft",
    client_id=os.getenv("MICROSOFT_CLIENT_ID"),
    client_secret=os.getenv("MICROSOFT_CLIENT_SECRET"),
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    authorize_params={
        "response_type": "code",
        "scope": "https://outlook.office365.com/IMAP.AccessAsUser.All",
    },
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    client_kwargs={"scope": "https://outlook.office365.com/IMAP.AccessAsUser.All"},
)


class AuthRequest(BaseModel):
    provider: str
    email: str = None
    password: str = None
    oauth_provider: str = None


@router.post("/auth/login")
async def login(request: Request, data: AuthRequest):
    """Authenticate using OAuth, email, or app-specific password."""
    if data.provider == "oauth":
        if data.oauth_provider not in ["google", "microsoft"]:
            raise HTTPException(status_code=400, detail="Invalid OAuth provider")

        redirect_uri = request.url_for(f"{data.oauth_provider}_callback")
        return await oauth.create_client(data.oauth_provider).authorize_redirect(
            request, redirect_uri
        )

    elif data.provider in ["email", "app_specific_password"]:
        # Use IMAP Authentication
        if not data.email or not data.password:
            raise HTTPException(
                status_code=400, detail="Email and password are required"
            )

        mail = email_imap.connect_imap(
            data.email, data.password, "gmail" if "gmail" in data.email else "outlook"
        )
        if "error" in mail:
            raise HTTPException(status_code=400, detail=mail["error"])

        emails = email_imap.fetch_recent_emails(mail)
        mail.logout()
        return {"message": "Login successful", "emails": emails}

    else:
        raise HTTPException(status_code=400, detail="Invalid provider type")


@router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback."""
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get(
        "https://www.googleapis.com/oauth2/v1/userinfo", token=token
    )
    return {"message": "Google OAuth login successful", "user": user_info.json()}


@router.get("/auth/microsoft/callback")
async def microsoft_callback(request: Request):
    """Handle Microsoft OAuth callback."""
    token = await oauth.microsoft.authorize_access_token(request)
    user_info = await oauth.microsoft.get(
        "https://graph.microsoft.com/v1.0/me", token=token
    )
    return {"message": "Microsoft OAuth login successful", "user": user_info.json()}
