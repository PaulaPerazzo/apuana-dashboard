import pandas as pd
import streamlit as st
from database.sheet_connection import get_sheet_df

@st.cache_data
def get_node_info_from_sheets(spreadsheet_id: str):
    df = get_sheet_df(spreadsheet_id, "node_state")
    
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    
    df = df.rename(columns={
        "hostname":     "hostname",
        "state":        "state",
        "last_updated": "last_updated",
    })
    
    df_node_info = (
        df
        .sort_values("last_updated", ascending=False)
        .head(50)
        .reset_index(drop=True)
    )
    
    return df_node_info
