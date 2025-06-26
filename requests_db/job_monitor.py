import pandas as pd
from database.sheet_connection import get_sheet_df
import streamlit as st

@st.cache_data
def get_job_monitor_requests_from_sheets(spreadsheet_id: str):
    df = get_sheet_df(spreadsheet_id, "job_log")
    
    df["submit"] = pd.to_datetime(df["submit"])
    df = df[df["submit"] >= pd.to_datetime("2025-01-01")]

    df["_date"] = df["submit"].dt.normalize()

    df_jobs_per_day = (
        df.groupby("_date")["jobid"]
        .nunique()
        .reset_index(name="count")
        .rename(columns={"_date": "submit"})
        .sort_values("submit", ascending=False)
    )

    print(df_jobs_per_day, "")
    
    df["elapsed_td"] = pd.to_timedelta(df["elapsed"])

    min_td  = df["elapsed_td"].min()
    mean_td = df["elapsed_td"].mean()
    max_td  = df["elapsed_td"].max()

    time_str      = str(min_td).split(".")[0]
    mean_time_str = str(mean_td).split(".")[0]
    max_time_str  = str(max_td).split(".")[0]
    
    df_top5 = (
        df
        .groupby("reqgpu")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .head(5)
    )
    
    df_plot_mem = (
        df
        .groupby("reqmem")
        .size()
        .reset_index(name="count")
    )
    df_plot_mem["reqmem"] = df_plot_mem["reqmem"].fillna("Desconhecido")
    df_plot_mem = df_plot_mem.sort_values("count", ascending=False).reset_index(drop=True)
    
    df_plot_cpu = (
        df
        .groupby("reqcpus")
        .size()
        .reset_index(name="count")
    )
    df_plot_cpu["reqcpus"] = df_plot_cpu["reqcpus"].fillna("Desconhecido")
    df_plot_cpu = df_plot_cpu.sort_values("count", ascending=False).reset_index(drop=True)
    
    return (
        df_jobs_per_day,
        time_str,
        mean_time_str,
        max_time_str,
        df_top5,
        df_plot_mem,
        df_plot_cpu
    )
