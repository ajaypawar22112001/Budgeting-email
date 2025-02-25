from authlib.integrations.starlette_client import OAuth
from config.settings import settings

oauth = OAuth()

# Google OAuth Config
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

# Microsoft OAuth Config
oauth.register(
    name="microsoft",
    client_id=settings.MICROSOFT_CLIENT_ID,
    client_secret=settings.MICROSOFT_CLIENT_SECRET,
    authorize_url="https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://login.microsoftonline.com/common/oauth2/v2.0/token",
    client_kwargs={"scope": "openid email profile"},
)
