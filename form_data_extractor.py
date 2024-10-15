import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
import re
import csv

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

def extract_form_data(content):
    # Define the fields we want to extract
    fields = ['Name', 'Email', 'Mobile', 'Address']
    data = {}

    # Extract data for each field
    for field in fields:
        pattern = rf'{field}:\s*(.*?)(?:\n|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            data[field] = match.group(1).strip()
        else:
            data[field] = ''

    return data

def validate_data(data):
    # Check if at least Name and Email are present
    return data['Name'] and data['Email']

def main():
    service = get_gmail_service()
    form_data_list = []

    for msg in get_emails(service, query="subject:'Email Extractor Test'"):
        content = extract_email_content(msg)
        form_data = extract_form_data(content)
        if validate_data(form_data):
            form_data_list.append(form_data)
        else:
            print(f"Skipping invalid data: {form_data}")

    # Write form data to CSV file
    if form_data_list:
        with open('form_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Email', 'Mobile', 'Address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in form_data_list:
                writer.writerow(data)

        print(f"Extracted form data from {len(form_data_list)} emails and saved to form_data.csv")
    else:
        print("No valid form data found in the emails.")

if __name__ == "__main__":
    main()
