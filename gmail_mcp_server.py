import os
import base64
from email.mime.text import MIMEText
from typing import Dict, Any, List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from mcp.server.fastmcp import FastMCP, Image
import sys


# Scopes for Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    """Initialize Gmail API service using OAuth2."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

service = get_gmail_service()

# Create FastMCP server
mcp = FastMCP("gmail-mcp")

# ---- Tools ----

@mcp.tool()
def send_email(to: str, subject: str, body: str, sender: str = "me") -> Dict[str, Any]:
    """
    Send an email using Gmail API.
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body (plain text)
        sender: Sender ("me" = authorized account)
    """
    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent = service.users().messages().send(userId=sender, body={"raw": raw}).execute()
    return {"message_id": sent["id"], "status": "sent"}

@mcp.tool()
def list_emails(max_results: int = 5) -> List[Dict[str, Any]]:
    """
    List recent email message IDs.
    Args:
        max_results: Number of emails to return (default 5).
    """
    results = service.users().messages().list(userId="me", maxResults=max_results).execute()
    return results.get("messages", [])

@mcp.tool()
def read_email(message_id: str) -> Dict[str, Any]:
    """
    Read an email by message ID.
    Args:
        message_id: The Gmail message ID to fetch.
    """
    msg = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    headers = msg["payload"]["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    body = ""

    # Extract plain text body
    if "data" in msg["payload"]["body"]:
        body = base64.urlsafe_b64decode(msg["payload"]["body"]["data"]).decode()
    elif "parts" in msg["payload"]:
        for part in msg["payload"]["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode()
                break

    return {"id": message_id, "from": sender, "subject": subject, "body": body}

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        print("RUNNING IN DEV MODE")
        mcp.run()  # Run without transport for dev server
    else:
        print("RUNNING IN PRODUCTION MODE")
        mcp.run(transport="stdio")  # Run with stdio for direct execution
