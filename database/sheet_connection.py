import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

@st.cache_data  # opcional
def get_sheet_df(spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
    creds = Credentials.from_service_account_file(
        "database/gen-lang-client-0851945156-1962f7fa2b9e.json", scopes=SCOPES
    )

    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    records = ws.get_all_records()

    print("get sheet id")

    return pd.DataFrame.from_records(records)
