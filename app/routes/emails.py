from app.services.email_service import fetch_emails
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/emails/fetch")
def fetch_email_data(
    email_provider: str, email_address: str, password: str, protocol: str = "IMAP"
):
    return fetch_emails(email_provider, email_address, password, protocol)
