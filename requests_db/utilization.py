import pandas as pd
import streamlit as st
from database.sheet_connection import get_sheet_df

@st.cache_data
def get_utilization_data_from_sheets(spreadsheet_id: str):
    df = get_sheet_df(spreadsheet_id, "utilization")

    for col in ["ocupation", "idle", "indisponibility"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )
    
    df["last_update"] = pd.to_datetime(df["last_update"])
    
    cutoff = pd.to_datetime("2024-01-01")
    df = df[df["last_update"] >= cutoff]
    
    df = df.sort_values("last_update", ascending=False).reset_index(drop=True)
    
    df_ocupation = (
        df[["last_update", "ocupation"]]
        .set_index("last_update")
    )
    df_idleness = (
        df[["last_update", "idle"]]
        .rename(columns={"idle": "idleness"})
        .set_index("last_update")
    )
    df_indisp = (
        df[["last_update", "indisponibility"]]
        .rename(columns={"indisponibility": "indisp"})
        .set_index("last_update")
    )
    
    return df_ocupation, df_idleness, df_indisp
