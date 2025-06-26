import textwrap
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit as st
import json

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

@st.cache_data  # opcional
def get_sheet_df(spreadsheet_id: str, sheet_name: str) -> pd.DataFrame:
    raw = st.secrets["google_json"]["service_account_info"]
    print(raw)
    cleaned = textwrap.dedent(raw).strip()  # tira indentação e espaços em volta
    cleaned = cleaned.replace("\n", "\\n")
    print(cleaned)
    
    # 2) carrega o JSON
    info = json.loads(cleaned)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)

    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    ws = sheet.worksheet(sheet_name)
    records = ws.get_all_records()

    return pd.DataFrame.from_records(records)

