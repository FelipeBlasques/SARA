import email
import imaplib
import keyring
from email.header import decode_header
from email.utils import parsedate_to_datetime
from email.message import EmailMessage
from logger import log
from config import email_destinatario, imap_server

def html_para_texto(html):
    import html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html)

def safe_decode(payload, encoding):
    try:
        return payload.decode(encoding)
    except UnicodeDecodeError:
        return payload.decode('latin1', errors='replace')

def connect_and_fetch_emails(email_user):
    email_pass = keyring.get_password("email", email_user)
    if not email_pass:
        raise ValueError(f"Senha não encontrada para {email_user}.")

    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_user, email_pass)
        mail.select("inbox")
        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        emails = []
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = EmailMessage()
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    from_ = msg.get("From")
                    date_ = parsedate_to_datetime(msg.get("Date"))
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type == "text/plain":
                                payload = part.get_payload(decode=True)
                                body = safe_decode(payload, part.get_content_charset() or 'utf-8')
                            elif content_type == "text/html":
                                payload = part.get_payload(decode=True)
                                html_body = safe_decode(payload, part.get_content_charset() or 'utf-8')
                                body = html_para_texto(html_body)
                    else:
                        content_type = msg.get_content_type()
                        payload = msg.get_payload(decode=True)
                        if content_type == "text/plain":
                            body = safe_decode(payload, msg.get_content_charset() or 'utf-8')
                        elif content_type == "text/html":
                            html_body = safe_decode(payload, msg.get_content_charset() or 'utf-8')
                            body = html_para_texto(html_body)

                    emails.append((subject, email_destinatario, date_, body))
        
        mail.close()
        mail.logout()
        log(f"Emails encontrados: {len(emails)}")
        return emails

    except Exception as e:
        log(f"Erro ao conectar ao servidor IMAP: {e}")
        raise e
