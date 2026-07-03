import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from cassandra.cluster import Cluster
from pymongo import MongoClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from config import CASSANDRA_HOST, CASSANDRA_KEYSPACE, CASSANDRA_PORT, MONGO_COLLECTION, MONGO_DATABASE, MONGO_URI

st.set_page_config(page_title="GitHub Events Big Data", layout="wide")
st.title("GitHub Events - Big Data Multimodel Analytics")

selected_date = st.sidebar.date_input("Fecha")
selected_date_text = selected_date.isoformat()


def mongo_event_count(event_date: str) -> int:
    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DATABASE][MONGO_COLLECTION]
    total = collection.count_documents({"event_date": event_date})
    client.close()
    return total


def cassandra_query(query: str, params: tuple) -> pd.DataFrame:
    cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
    session = cluster.connect(CASSANDRA_KEYSPACE)
    rows = session.execute(query, params)
    df = pd.DataFrame(list(rows))
    cluster.shutdown()
    return df


try:
    total_mongo = mongo_event_count(selected_date_text)
    kpis = cassandra_query("SELECT * FROM kpis_by_day WHERE event_date = %s", (selected_date,))
    events = cassandra_query(
        "SELECT event_type, event_hour, total_events FROM events_by_day_type WHERE event_date = %s",
        (selected_date,),
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Eventos en MongoDB", total_mongo)

    if not kpis.empty:
        row = kpis.iloc[0]
        c2.metric("Usuarios únicos", int(row["unique_actors"]))
        c3.metric("Repositorios únicos", int(row["unique_repositories"]))
        st.metric("Tipo de evento dominante", row["top_event_type"])
    else:
        c2.metric("Usuarios únicos", 0)
        c3.metric("Repositorios únicos", 0)
        st.info("Aún no hay KPIs en Cassandra para esta fecha.")

    st.subheader("Eventos por hora y tipo")
    if events.empty:
        st.info("No hay eventos agregados para la fecha seleccionada.")
    else:
        fig = px.line(events, x="event_hour", y="total_events", color="event_type", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(events, use_container_width=True)

except Exception as error:
    st.error("No se pudo conectar a las bases de datos. Verifica Docker y las variables de entorno.")
    st.write(str(error))
