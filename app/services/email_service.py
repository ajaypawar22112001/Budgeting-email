import datetime
import email
import imaplib
from email.header import decode_header

from app.utils.db import email_collection


def fetch_emails(email_provider, email_address, password, protocol="IMAP"):
    if protocol.upper() == "IMAP":
        mail = imaplib.IMAP4_SSL(email_provider)
        mail.login(email_address, password)
        mail.select("inbox")

        date_since = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime(
            "%d-%b-%Y"
        )
        result, data = mail.search(None, f"SINCE {date_since}")
        email_ids = data[0].split()

        emails_metadata = []
        for email_id in email_ids:
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding:
                        subject = subject.decode(encoding)
                    sender = msg.get("From")
                    date = msg.get("Date")

                    email_metadata = {
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "raw_email": msg.as_string(),
                    }
                    emails_metadata.append(email_metadata)
                    email_collection.insert_one(email_metadata)

        mail.logout()
        return {"fetched": len(emails_metadata), "details": emails_metadata}
