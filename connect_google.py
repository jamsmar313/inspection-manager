
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS = BASE_DIR / "google_credentials.json"
TOKEN = BASE_DIR / "google_token.json"

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

if not CREDENTIALS.exists():
    raise FileNotFoundError(
        f"Missing {CREDENTIALS}. Check the credentials filename."
    )

flow = InstalledAppFlow.from_client_secrets_file(
    str(CREDENTIALS),
    SCOPES,
)

credentials = flow.run_local_server(
    host="localhost",
    port=0,
    open_browser=True,
)

TOKEN.write_text(credentials.to_json())
TOKEN.chmod(0o600)

service = build("calendar", "v3", credentials=credentials)

# Verify access using the permission already granted.
service.events().list(
    calendarId="primary",
    maxResults=1
).execute()

print("SUCCESS! Google Calendar connected.")
print("Calendar event access verified.")
print("Credentials saved to:", TOKEN)
