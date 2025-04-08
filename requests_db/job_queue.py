import pandas as pd

def get_jobs_queue(conn):
    df_jobs_queue = pd.read_sql(
        'SELECT jobid AS JOBID, name AS NAME, nodelist AS NODELIST, "USER", state AS STATE, last_updated FROM queue ORDER BY last_updated DESC LIMIT 50',
        conn
    )

    return df_jobs_queue
