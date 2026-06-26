import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backend.logger import setup_logging
from datetime import datetime
from backend.fetcher import fetch_pv_data
from backend.cleaner import clean_pv_data
from backend.storage import (
    init_storage,
    save_reading,
    get_readings_for_day,
)
from backend.calculator import calculate_daily, calculate_monthly, calculate_yearly


def main():
    setup_logging()
    st.title("☀️ Suntrack — PV Dashboard")

    init_storage()

    # Fetch and save latest reading
    raw = fetch_pv_data()
    data = clean_pv_data(raw)
    if data:
        save_reading(data)

    # Momentanwerte
    st.header("⚡ Momentanwerte")
    col1, col2 = st.columns(2)
    col1.metric("Erzeugung (W)", round(data.get("generation_w", 0), 2))
    col2.metric("Verbrauch (W)", round(data.get("consumption_w", 0), 2))

    # Tageswerte
    st.header("📅 Tageswerte")
    today = datetime.now()
    daily = calculate_daily(today)
    if daily:
        col1, col2, col3 = st.columns(3)
        col1.metric("Erzeugung (W)", round(daily["total_generation_w"], 2))
        col2.metric("Verbrauch (W)", round(daily["total_consumption_w"], 2))
        col3.metric("PV-Anteil (%)", daily["pv_ratio_percent"])

    # Monatswerte
    st.header("📆 Monatswerte")
    monthly = calculate_monthly(today.year, today.month)
    if monthly:
        col1, col2, col3 = st.columns(3)
        col1.metric("Erzeugung (W)", round(monthly["total_generation_w"], 2))
        col2.metric("Verbrauch (W)", round(monthly["total_consumption_w"], 2))
        col3.metric("PV-Anteil (%)", monthly["pv_ratio_percent"])

    # Jahreswerte
    st.header("📊 Jahreswerte")
    yearly = calculate_yearly(today.year)
    if yearly:
        col1, col2, col3 = st.columns(3)
        col1.metric("Erzeugung (W)", round(yearly["total_generation_w"], 2))
        col2.metric("Verbrauch (W)", round(yearly["total_consumption_w"], 2))
        col3.metric("PV-Anteil (%)", yearly["pv_ratio_percent"])

    # Zeitverlauf
    st.header("📈 Zeitverlauf")
    readings = get_readings_for_day(today)
    if readings:
        df = pd.DataFrame(readings)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["generation_w"] = df["generation_w"].astype(float)
        df["consumption_w"] = df["consumption_w"].astype(float)
        st.line_chart(df.set_index("timestamp")[["generation_w", "consumption_w"]])

    # Tortendiagramme
    st.header("🥧 PV-Anteil")
    col1, col2, col3 = st.columns(3)

    if daily:
        pv = daily["pv_ratio_percent"]
        rest = round(100 - pv, 2)
        fig = go.Figure(go.Pie(labels=["PV", "Netz"], values=[pv, rest]))
        fig.update_layout(title="Tag")
        col1.plotly_chart(fig, use_container_width=True)

    if monthly:
        pv = monthly["pv_ratio_percent"]
        rest = round(100 - pv, 2)
        fig = go.Figure(go.Pie(labels=["PV", "Netz"], values=[pv, rest]))
        fig.update_layout(title="Monat")
        col2.plotly_chart(fig, use_container_width=True)

    if yearly:
        pv = yearly["pv_ratio_percent"]
        rest = round(100 - pv, 2)
        fig = go.Figure(go.Pie(labels=["PV", "Netz"], values=[pv, rest]))
        fig.update_layout(title="Jahr")
        col3.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
