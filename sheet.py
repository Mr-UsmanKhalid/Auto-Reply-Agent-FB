import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def load_faq():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Load from env var (Vercel) or fall back to file (local)
    creds_json = os.environ.get("GOOGLE_CREDS_JSON")

    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            creds_dict,
            scope
        )
    else:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "creds.json",
            scope
        )

    client = gspread.authorize(creds)

    sheet = client.open_by_key(
        "1dDy4SVGR5dOTBU1ckM5HCrhH6oJwDA3gdHP2B68NvVM"
    ).sheet1

    data = sheet.get_all_records()

    faq = {}

    for row in data:
        faq[row["keyword"].lower()] = row["reply"]

    return faq