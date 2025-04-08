import pandas as pd

def get_utilization_data(conn):
    ### GET OCCUPATION
    df_ocupation = pd.read_sql(
        "SELECT ocupation, last_update FROM utilization WHERE last_update >= '01-01-2024' ORDER BY last_update DESC",
        conn
    )

    ### GET IDLENESS
    df_idleness = pd.read_sql(
        "SELECT idle, last_update FROM utilization WHERE last_update >= '01-01-2024' ORDER BY last_update DESC",
        conn
    )

    ### GET INDISPONIBILITY
    df_indisp = pd.read_sql(
        "SELECT indisponibility, last_update FROM utilization WHERE last_update >= '01-01-2024' ORDER BY last_update DESC",
        conn
    )

    return df_ocupation, df_idleness, df_indisp
