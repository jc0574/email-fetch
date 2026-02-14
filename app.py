import imaplib
import email
import os
from dotenv import find_dotenv, load_dotenv



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("PASSWORD")

if EMAIL_ADDRESS is None or PASSWORD is None:
    raise ValueError("Missing EMAIL_ADDRESS or PASSWORD in .env")

imap_server = "imap.gmail.com"
imap = imaplib.IMAP4_SSL(imap_server)
imap.login(EMAIL_ADDRESS, PASSWORD) 

imap.select('"[Gmail]/Sent Mail"')
_, msgnums = imap.search(None, "ALL")
all_ids = msgnums[0].split()
newest_10 = all_ids[-10:]


for id in reversed(newest_10):
    _, data = imap.fetch(id, "(RFC822)")
    message = email.message_from_bytes(data[0][1]) # type: ignore

    print(f"Message ID: {id}")
    print(f"Subject: {message.get('Subject')}")
    print(f"From: {message.get('From')}")
    print(f"To: {message.get('To')}")
    print(f"BCC: {message.get('BCC')}")
    print(f"Date: {message.get('Date')}")

    print("Content: ")
    for part in message.walk():
        if part.get_content_type() == "text/plain" :
            print(part.as_string())
    
imap.close()
imap.logout()
