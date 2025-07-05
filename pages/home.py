import streamlit as st
from utils.data_loader import (
    get_tourism_annual_summary,
    get_forex_earnings_summary,
    get_recovery_speed_by_year,
    get_peak_tourism_months,
    get_highest_growth_year,
    get_lowest_growth_year,
)

st.title("📊 India’s Culture & Tourism Dashboard")
st.markdown("An interactive dashboard exploring India's cultural investment and tourism trends (2019–2024).")

st.header("🗓️ Annual Tourism Earnings")
tourism = get_tourism_annual_summary()
st.bar_chart(tourism.set_index("year"))

st.header("💸 Forex Earnings from Tourism")
forex = get_forex_earnings_summary()
st.line_chart(forex.set_index("year"))

st.header("📈 Recovery Speed (YoY Growth)")
growth = get_recovery_speed_by_year()
st.dataframe(growth)

col1, col2 = st.columns(2)
with col1:
    st.metric("Highest Growth Year", int(get_highest_growth_year()["year"]), f"{get_highest_growth_year()['yoy_growth_pct'].values[0]}%")
with col2:
    lowest = get_lowest_growth_year()
    st.metric("Lowest Growth Year", int(lowest["year"]), f"{lowest['yoy_growth_pct'].values[0]}%")
