import pandas as pd
import streamlit as st
from database.sheet_connection import get_sheet_df

@st.cache_data
def get_jobs_queue_from_sheets(spreadsheet_id: str):
    df = get_sheet_df(spreadsheet_id, "queue")
    
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    
    df = df.rename(columns={
        "jobid":      "JOBID",
        "name":       "NAME",
        "nodelist":   "NODELIST",
        "user":       "USER",
        "state":      "STATE",
    })
    
    df_jobs_queue = (
        df
        .sort_values("last_updated", ascending=False)
        .head(50)
        .reset_index(drop=True)
    )
    
    return df_jobs_queue
