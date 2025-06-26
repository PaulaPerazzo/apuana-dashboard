import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

@st.cache_data  # opcional
def get_sheet_df(spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
    info = json.loads(st.secrets["google_sheets"]["service_account_info"])

    creds = Credentials.from_service_account_file(info, scopes=SCOPES)

    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    records = ws.get_all_records()

    return pd.DataFrame.from_records(records)
