import email
import imaplib
from email.header import decode_header
from typing import List


def connect_imap(email_address: str, password: str, provider: str):
    """Connects to the IMAP server and authenticates the user."""
    imap_server = {"gmail": "imap.gmail.com", "outlook": "outlook.office365.com"}.get(
        provider, None
    )

    if not imap_server:
        return {"error": "Unsupported email provider"}

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, password)
        return mail
    except Exception as e:
        return {"error": str(e)}


def fetch_recent_emails(mail, mailbox="INBOX", limit=10) -> List[dict]:
    """Fetches recent emails from the specified mailbox."""
    mail.select(mailbox)
    _, messages = mail.search(None, "ALL")
    message_ids = messages[0].split()[-limit:]

    emails = []
    for msg_id in message_ids:
        _, msg_data = mail.fetch(msg_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg["Subject"])[0]
                subject = subject.decode(encoding) if encoding else subject
                emails.append({"subject": subject, "from": msg["From"]})

    return emails
