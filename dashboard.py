from database.database_connection import get_database_connection
import streamlit as st
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from requests_db.job_monitor import get_job_monitor_requests
from requests_db.utilization import get_utilization_data
from requests_db.system_monitor import get_system_monitor_requests
from requests_db.job_queue import get_jobs_queue
from requests_db.node_info import get_node_info

conn = get_database_connection()

# ============= QUERIES ============= #

df_jobs_per_day, time_str, mean_time_str, max_time_str, df_top5, df_plot_mem, df_plot_cpu = get_job_monitor_requests(conn)
df_ocupation, df_idleness, df_indisp = get_utilization_data(conn)
df_temp, df_mem_usage, _ = get_system_monitor_requests(conn)
df_job_queue = get_jobs_queue(conn)
df_node_info = get_node_info(conn)

# ============= DASHBOARD ============= #

st.set_page_config(layout="wide")
st.title("Apuana Dashboard")

####### JOB MONITOR #######
st.subheader("Job Monitor")

# jobs per day
st.write("Lançamentos de Jobs por Dia")
st.line_chart(df_jobs_per_day.set_index('submit'), width=1000, height=300, use_container_width=True)

# min, mean and max jobs exec time
st.write("Tempo de Execução dos Jobs")
st.markdown("""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: row;
        gap: 20px;
        background-color: transparent;
        padding: 8px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 16px;
        font-family: 'Courier New', monospace;
        font-weight: bold;">
        <div>Tempo mínimo de execução <br><span style="font-size: 24px;">""" + time_str + """</span></div>
        <div>Tempo médio de execução <br><span style="font-size: 24px;">""" + mean_time_str + """</span></div>
        <div>Tempo máximo de execução <br><span style="font-size: 24px;">""" + max_time_str + """</span></div>
    </div>
""", unsafe_allow_html=True)

# gpu requests
fig = px.pie(
    df_top5,
    names='reqgpu',
    values='count',
    hole=0,
)

# memory request
chart_mem = (
    alt.Chart(df_plot_mem[:10])
    .mark_bar()
    .encode(
        x=alt.X('reqmem:N', sort=None, title='Memória (GB)'),
        y=alt.Y('count:Q', title='Número de Requisições'),
        tooltip=['reqmem', 'count']
    )
    .properties(
        width=600, 
        height=200
    )
)

# cpu request
chart_cpu = (
    alt.Chart(df_plot_cpu[:10])
    .mark_bar()
    .encode(
        x=alt.X('reqcpus:N', sort=None, title='CPUs'),
        y=alt.Y('count:Q', title='Número de Requisições'),
        tooltip=['reqcpus', 'count']
    )
    .properties(
        width=600, 
        height=200
    )
)

col1, col2 = st.columns([1, 1])

with col1:
    st.write("Requisições de GPU")
    st.plotly_chart(fig, use_container_width=False)

with col2:
    st.write("Requisições de Memória")
    st.altair_chart(chart_mem, use_container_width=False)
    st.write("Requisições de CPU")
    st.altair_chart(chart_cpu, use_container_width=False)

######## UTILIZATION ########
st.subheader("Utilização")

# ocupation
st.write("Ocupação (%)")
st.line_chart(df_ocupation.set_index('last_update'), width=1300, height=300, use_container_width=True)

# idleness
st.write("Ociosidade (%)")
st.line_chart(df_idleness.set_index('last_update'), width=1300, height=300, use_container_width=True)

# unavailability
st.write("Indisponibilidade (%)")
st.line_chart(df_indisp.set_index('last_update'), width=1300, height=300, use_container_width=True)

######## SYSTEM MONITOR ########
st.subheader("Monitoramento do Sistema")

# nodes temperature
temp_max = df_temp['temp_max'].mean()
temp_mean = df_temp['temp_mean'].mean()
temp_min = df_temp['temp_min'].mean()

fig_temp = make_subplots(
    rows=1, cols=3, 
    specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
    subplot_titles=("temp_max", "temp_mean", "temp_min")
)

# 1) Gauge for temp_max
fig_temp.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=temp_max,
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "orange"} 
        }
    ),
    row=1, col=1
)

# 2) Gauge for temp_mean
fig_temp.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=temp_mean,
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "green"}
        }
    ),
    row=1, col=2
)

# 3) Gauge for temp_min
fig_temp.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=temp_min,
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "green"}
        }
    ),
    row=1, col=3
)

fig_temp.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=60, b=20),
)

mem_max = df_mem_usage['mem_max'].mean()
mem_min = df_mem_usage['mem_min'].mean()

fig_usage = make_subplots(
    rows=1, cols=2, 
    specs=[[{"type": "domain"}, {"type": "domain"}]],
    subplot_titles=("mem_max", "mem_min")
)

# 1) Gauge for mem_max
fig_usage.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=mem_max,
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "orange"} 
        }
    ),
    row=1, col=1
)

# 2) Gauge for mem_min
fig_usage.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=mem_min,
        gauge={
            "axis": {"range": [None, 100]},
            "bar": {"color": "green"}
        }
    ),
    row=1, col=2
)

fig_usage.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=60, b=20),
)

col1_sys, col2_sys = st.columns([3, 2])

with col1_sys:
    st.write("Temperatura dos Nodos")
    st.plotly_chart(fig_temp, use_container_width=True)

with col2_sys:
    st.write("Consumo de Memória (MiB)")
    st.plotly_chart(fig_usage, use_container_width=True)

# storage
# st.write("Armazenamento Diário (%)")
# st.line_chart(df_store.set_index('time'), width=1300, height=300, use_container_width=True)

# queue
st.subheader("Fila de Jobs")
st.write("Queue")
page_size = 10
total_rows = len(df_job_queue)
total_pages = (total_rows - 1) // page_size + 1

page = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1)

start_idx = (page - 1) * page_size
end_idx = start_idx + page_size

st.dataframe(df_job_queue.iloc[start_idx:end_idx])

# node info
st.subheader("Informações dos Nodos")
st.write("Node Info")

st.dataframe(df_node_info.iloc[:10])

conn.close()
