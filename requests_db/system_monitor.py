import pandas as pd
import streamlit as st
from database.sheet_connection import get_sheet_df

@st.cache_data
def get_system_monitor_requests_from_sheets(spreadsheet_id: str):
    df_gpu = get_sheet_df(spreadsheet_id, "gpu_log")
    
    df_gpu["temperature_gpu"] = pd.to_numeric(df_gpu["temperature_gpu"], errors="coerce")
    df_gpu["memory_used"]     = pd.to_numeric(df_gpu["memory_used"], errors="coerce")
    
    df_temp = (
        df_gpu
        .groupby("hostname", as_index=False)
        .agg(
            temp_max  = pd.NamedAgg(column="temperature_gpu", aggfunc="max"),
            temp_mean = pd.NamedAgg(column="temperature_gpu", aggfunc="mean"),
            temp_min  = pd.NamedAgg(column="temperature_gpu", aggfunc="min"),
        )
        .head(50)
    )
    
    df_mem_usage = (
        df_gpu
        .groupby("hostname", as_index=False)
        .agg(
            mem_max = pd.NamedAgg(column="memory_used", aggfunc="max"),
            mem_min = pd.NamedAgg(column="memory_used", aggfunc="min"),
        )
        .head(50)
    )

    df_mem_usage["mem_max"] = df_mem_usage["mem_max"] / 1024 # convert to MiB
    df_mem_usage["mem_min"] = df_mem_usage["mem_min"] / 1024
    
    df_store = get_sheet_df(spreadsheet_id, "filesystem_data")
    df_store = df_store[df_store["mounted"] == "/home/CIN"]

    df_store["time"]       = pd.to_datetime(df_store["time"], errors="coerce")
    df_store["use"]        = pd.to_numeric(df_store["usepercent"], errors="coerce")
    df_store = df_store[["time", "use"]]
    
    return df_temp, df_mem_usage, df_store
