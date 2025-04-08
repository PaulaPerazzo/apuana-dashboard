import pandas as pd

def get_job_monitor_requests(conn):
    ### GET JOBS PER DAY 
    df_jobs_per_day = pd.read_sql(
        "SELECT submit, COUNT(jobid) FROM job_log WHERE submit >= '2025-01-01' GROUP BY submit ORDER BY submit DESC",
        conn
    )

    ### GET MIN TIME JOBS
    df_min_exec_time = pd.read_sql(
        "SELECT MIN(elapsed) AS min_elapsed FROM job_log LIMIT 50",
        conn
    )
    min_seconds = df_min_exec_time.loc[0, 'min_elapsed']
    time_str = str(min_seconds).split(".")[0] 

    ### GET MEAN EXEC TIME 
    df_mean_exec_time = pd.read_sql(
        "SELECT AVG(elapsed) AS mean_elapsed FROM job_log LIMIT 50",
        conn
    )
    mean_seconds = df_mean_exec_time.loc[0, 'mean_elapsed']
    mean_time_str = str(mean_seconds).split(".")[0]  

    ### GET MAX EXEC TIME 
    df_max_exec_time = pd.read_sql(
        "SELECT MAX(elapsed) AS max_elapsed FROM job_log LIMIT 50",
        conn
    )
    max_seconds = df_max_exec_time.loc[0, 'max_elapsed']
    max_time_str = str(max_seconds).split(".")[0] 

    ### GET GPU REQUESTS
    df_gpu_requests = pd.read_sql(
        "SELECT reqgpu, count(reqgpu) as count FROM job_log GROUP BY reqgpu",
        conn
    )
    df_top5 = df_gpu_requests.sort_values(by='count', ascending=False).head(5)

    ### GET MEMORY REQUESTS
    df_mem_requests = pd.read_sql(
        "SELECT reqmem, COUNT(*) AS count FROM job_log GROUP BY reqmem LIMIT 50",
        conn
    )
    df_mem_requests['reqmem'] = df_mem_requests['reqmem'].fillna('Desconhecido')
    df_mem_requests = df_mem_requests.sort_values(by='count', ascending=False)
    df_plot_mem = df_mem_requests.reset_index(drop=True)

    ### GET CPU REQUESTS
    df_cpu_requests = pd.read_sql(
        "SELECT reqcpus, COUNT(*) AS count FROM job_log GROUP BY reqcpus LIMIT 50",
        conn
    )
    df_cpu_requests['reqcpus'] = df_cpu_requests['reqcpus'].fillna('Desconhecido')
    df_cpu_requests = df_cpu_requests.sort_values(by='count', ascending=False)
    df_plot_cpu = df_cpu_requests.reset_index(drop=True)

    return df_jobs_per_day, time_str, mean_time_str, max_time_str, df_top5, df_plot_mem, df_plot_cpu
