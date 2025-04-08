import pandas as pd

def get_node_info(conn):
    df_node_info = pd.read_sql(
        'SELECT hostname, state, last_updated FROM node_state ORDER BY last_updated DESC LIMIT 50',
        conn
    )

    return df_node_info