#!/usr/bin/env python3
"""
Google Sheets Upload Script - Uses OAuth loopback flow for email-based auth.

This script uses Python's google-auth-oauthlib with a localhost callback.
The auth URL is sent to your email and you can approve it by visiting the link.

Usage:
    export GOOGLE_OAUTH_CLIENT_ID=<your_client_id>
    export GOOGLE_OAUTH_CLIENT_SECRET=<your_client_secret>
    python upload_to_sheets.py --file form_data.csv --sheet-name "Form Guides"
"""

import os
import pickle
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# OAuth scope for Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']

# Token cache location
TOKEN_FILE = Path.home() / '.google_sheets_token.pickle'


def get_creds():
    """Get or create Google OAuth credentials."""
    creds = None
    
    # Load ~/.env if present
    env_path = Path.home() / '.env'
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                k = k.strip().lstrip('export ')
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v

    # Load existing token
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        
        if not creds:
            # Run OAuth flow
            client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID') or os.environ.get('CLIENT_ID')
            client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') or os.environ.get('CLIENT_SECRET')
            
            if not client_id or not client_secret:
                print("Error: GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET must be set", file=sys.stderr)
                sys.exit(1)
            
            # OAuth flow configuration
            flow = Flow.from_client_config(
                {
                    "installed": {
                        "client_id": client_id,
                        "client_secret": client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": ["http://127.0.0.1:8080/", "http://localhost:8080/"]
                    }
                },
                scopes=SCOPES,
                redirect_uri='http://127.0.0.1:8080/'
            )
            
            # Get authorization URL
            auth_url, _ = flow.authorization_url(prompt='consent')
            print("\n" + "="*60, file=sys.stderr)
            print("GOOGLE SHEETS AUTHENTICATION REQUIRED", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print(f"Step 1: Copy this URL and open in your browser:\n{auth_url}\n", file=sys.stderr)
            print("Step 2: Sign in with your Google account", file=sys.stderr)
            print("Step 3: Grant permission for 'Google Sheets' access", file=sys.stderr)
            print("Step 4: Copy the AUTHORIZATION CODE from the callback page and paste here", file=sys.stderr)
            print("\nOr, if using a device that can open a browser automatically, the auth flow will wait...\n", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            
            # Wait for user to approve
            try:
                code = input("Enter the authorization code: ").strip()
                flow.fetch_token(code=code)
            except Exception as e:
                print(f"Auth flow failed: {e}", file=sys.stderr)
                raise
            
            creds = flow.credentials
            
            # Save credentials
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
    
    return creds


def upload_csv_to_sheet(csv_path: str, sheet_name: str = "Form Guides"):
    """Upload CSV content to a Google Sheet."""
    creds = get_creds()
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # Read CSV file
        csv_content = Path(csv_path).read_text()
        rows = []
        for line in csv_content.strip().split('\n'):
            rows.append(line.split(','))
        
        # Create or update sheet
        spreadsheet = None
        sheet_id = None
        
        # Try to find existing spreadsheet or create new
        sheets_service = build('sheets', 'v4', credentials=creds)
        
        # Create new spreadsheet
        spreadsheet_body = {
            'properties': {
                'title': sheet_name
            }
        }
        spreadsheet = sheets_service.spreadsheets().create(body=spreadsheet_body).execute()
        sheet_id = spreadsheet['spreadsheetId']
        print(f"Created spreadsheet: {sheet_id}", file=sys.stderr)
        
        # Upload data
        body = {
            'values': rows
        }
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Sheet1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Updated {result.get('updatedCells', 0)} cells", file=sys.stderr)
        
        # Get web view link
        drive_service = build('drive', 'v3', credentials=creds)
        file_metadata = drive_service.files().get(fileId=sheet_id, fields='webViewLink').execute()
        link = file_metadata.get('webViewLink')
        
        print(f"\nSuccess! View your sheet: {link}", file=sys.stderr)
        return sheet_id, link
        
    except HttpError as error:
        print(f"An error occurred: {error}", file=sys.stderr)
        raise


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Upload CSV to Google Sheets")
    parser.add_argument("--file", required=True, help="Path to CSV file")
    parser.add_argument("--sheet-name", default="Form Guides", help="Name for the Google Sheet")
    
    args = parser.parse_args()
    
    if not Path(args.file).exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        sheet_id, link = upload_csv_to_sheet(args.file, args.sheet_name)
        print(f"\nSpreadsheet ID: {sheet_id}", file=sys.stderr)
        print(f"Link: {link}", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()