import pandas as pd

def get_system_monitor_requests(conn):
    ### GET NODES TEMPERATURE
    df_temp = pd.read_sql(
        "SELECT hostname, MAX(temperature_gpu) AS temp_max, AVG(temperature_gpu) AS temp_mean, MIN(temperature_gpu) AS temp_min " \
        "FROM gpu_log GROUP BY hostname LIMIT 50 ",
        conn
    )

    ### GET MEM USAGE
    df_mem_usage = pd.read_sql(
        "SELECT MAX(memory_used) AS mem_max, MIN(memory_used) AS mem_min FROM gpu_log GROUP BY hostname LIMIT 50 ",
        conn
    )
    df_mem_usage['mem_max'] = df_mem_usage['mem_max'].astype(float)
    df_mem_usage['mem_min'] = df_mem_usage['mem_min'].astype(float)

    ### GET STORED DATA
    df_store = pd.read_sql(
        "SELECT usepercent AS use, time FROM filesystem_data",
        conn
    )

    return df_temp, df_mem_usage, df_store
