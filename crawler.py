import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def get_emails(service, query=""):
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        yield msg

def extract_email_content(msg):
    payload = msg['payload']
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode()
    elif 'body' in payload:
        data = payload['body']['data']
        return base64.urlsafe_b64decode(data).decode()
    return ""

def main():
    service = get_gmail_service()
    email_contents = []

    for msg in get_emails(service, query="subject:'REPLACE WITH EMAIL SUBJECT'"):
        content = extract_email_content(msg)
        email_contents.append(content)

    # Write all email contents to a single text file
    with open('email_contents.txt', 'w', encoding='utf-8') as f:
        for content in email_contents:
            f.write(content + "\n\n" + "-"*50 + "\n\n")  # Separator between emails

    print(f"Extracted content from {len(email_contents)} emails and saved to email_contents.txt")

if __name__ == "__main__":
    main()
