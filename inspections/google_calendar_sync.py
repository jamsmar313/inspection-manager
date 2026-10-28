
from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN_FILE = Path(settings.BASE_DIR) / "google_token.json"


def calendar_service():
    if not TOKEN_FILE.exists():
        raise RuntimeError(
            "Google Calendar is not connected. "
            "Run python connect_google.py first."
        )

    credentials = Credentials.from_authorized_user_file(
        str(TOKEN_FILE), SCOPES
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        TOKEN_FILE.write_text(credentials.to_json())
        TOKEN_FILE.chmod(0o600)

    if not credentials.valid:
        raise RuntimeError("Google Calendar authorization expired.")

    return build("calendar", "v3", credentials=credentials)


def sync_inspection(job):
    """Create or update a Google Calendar appointment."""
    if not job.scheduled_at:
        return None

    start = job.scheduled_at

    if timezone.is_naive(start):
        start = timezone.make_aware(
            start, timezone.get_current_timezone()
        )

    end = start + timedelta(minutes=90)

    event = {
        "summary": f"Inspection #{job.job_number} - {job.insured_name}",
        "location": job.property_address or "",
        "description": "\n".join(filter(None, [
            f"Job: {job.job_number}",
            f"Insured: {job.insured_name}",
            f"Phone: {job.phone}",
            f"Status: {job.status}",
            f"Notes: {job.contact_notes}",
        ])),
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": end.isoformat()},
    }

    service = calendar_service()

    if job.calendar_event_id:
        result = service.events().update(
            calendarId="primary",
            eventId=job.calendar_event_id,
            body=event,
        ).execute()
    else:
        result = service.events().insert(
            calendarId="primary",
            body=event,
        ).execute()

        job.calendar_event_id = result["id"]
        job.save(update_fields=["calendar_event_id"])

    return result.get("htmlLink")
