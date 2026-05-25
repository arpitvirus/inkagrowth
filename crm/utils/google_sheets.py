import logging
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from django.utils import timezone

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    gspread = None
    Credentials = None


logger = logging.getLogger(__name__)

GOOGLE_SHEETS_SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets',
)

LEAD_SHEET_HEADERS = [
    'Lead ID',
    'Name',
    'Email',
    'Phone',
    'Company Name',
    'Lead Status',
    'Created Date',
]


@dataclass(frozen=True)
class GoogleSheetSyncResult:
    success: bool
    skipped: bool
    message: str


def sync_lead_to_google_sheet(lead):
    """
    Append a newly created lead to Google Sheets.

    The function is intentionally fail-safe: CRM lead creation must not fail
    because an external integration is missing, slow, or temporarily down.
    """
    if not getattr(settings, 'GOOGLE_SHEETS_SYNC_ENABLED', False):
        return GoogleSheetSyncResult(
            success=False,
            skipped=True,
            message='Google Sheets sync is disabled.',
        )

    if gspread is None or Credentials is None:
        logger.warning(
            'Google Sheets sync skipped because gspread/google-auth is not installed.'
        )
        return GoogleSheetSyncResult(
            success=False,
            skipped=True,
            message='gspread/google-auth is not installed.',
        )

    spreadsheet_id = getattr(settings, 'GOOGLE_SHEETS_SPREADSHEET_ID', '')
    if not spreadsheet_id:
        logger.warning('Google Sheets sync skipped because spreadsheet ID is missing.')
        return GoogleSheetSyncResult(
            success=False,
            skipped=True,
            message='Google Sheets spreadsheet ID is missing.',
        )

    credentials_path = get_credentials_path()
    if not credentials_path.exists():
        logger.warning(
            'Google Sheets sync skipped because credentials file was not found: %s',
            credentials_path,
        )
        return GoogleSheetSyncResult(
            success=False,
            skipped=True,
            message='Google Sheets credentials file is missing.',
        )

    try:
        worksheet = get_leads_worksheet(credentials_path, spreadsheet_id)
        ensure_lead_sheet_headers(worksheet)
        worksheet.append_row(
            values=format_lead_row(lead),
            value_input_option='USER_ENTERED',
        )
    except Exception:
        logger.exception('Google Sheets sync failed for lead %s.', lead.pk)
        return GoogleSheetSyncResult(
            success=False,
            skipped=False,
            message='Google Sheets sync failed.',
        )

    return GoogleSheetSyncResult(
        success=True,
        skipped=False,
        message='Lead synced to Google Sheets.',
    )


def get_credentials_path():
    credentials_file = getattr(settings, 'GOOGLE_SHEETS_CREDENTIALS_FILE', '')
    credentials_path = Path(credentials_file)

    if credentials_path.is_absolute():
        return credentials_path

    return Path(settings.BASE_DIR) / credentials_path


def get_google_sheets_client(credentials_path):
    credentials = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=GOOGLE_SHEETS_SCOPES,
    )
    return gspread.authorize(credentials)


def get_leads_worksheet(credentials_path, spreadsheet_id):
    client = get_google_sheets_client(credentials_path)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet_name = getattr(settings, 'GOOGLE_SHEETS_WORKSHEET_NAME', 'Leads')

    try:
        return spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        return spreadsheet.add_worksheet(
            title=worksheet_name,
            rows=1000,
            cols=len(LEAD_SHEET_HEADERS),
        )


def ensure_lead_sheet_headers(worksheet):
    header_range = f'A1:{column_letter(len(LEAD_SHEET_HEADERS))}1'
    existing_headers = worksheet.row_values(1)

    if existing_headers[:len(LEAD_SHEET_HEADERS)] == LEAD_SHEET_HEADERS:
        return

    worksheet.update(
        values=[LEAD_SHEET_HEADERS],
        range_name=header_range,
    )


def format_lead_row(lead):
    created_at = timezone.localtime(lead.created_at).strftime('%Y-%m-%d %H:%M:%S')

    return [
        str(lead.pk),
        lead.name,
        lead.email or '',
        lead.phone or '',
        lead.company_name or '',
        lead.get_status_display(),
        created_at,
    ]


def column_letter(column_number):
    letters = ''

    while column_number:
        column_number, remainder = divmod(column_number - 1, 26)
        letters = chr(65 + remainder) + letters

    return letters
