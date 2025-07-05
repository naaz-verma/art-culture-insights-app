# ✅ pages/trends.py
import streamlit as st
import plotly.express as px
from utils.data_loader import (
    get_tourism_monthly_avg,
    get_peak_tourism_months,
    get_funding_by_year,
    get_funding_by_agency,
    get_funding_vs_tourism_by_year,
    get_india_vs_world_growth,
    get_india_global_share_trend,
)

st.title("📊 Trends in Tourism, Funding & Global Standing")

# Section 1: Monthly Tourism Patterns
st.header("🗓️ Monthly Tourism Averages")
monthly_avg = get_tourism_monthly_avg()
fig1 = px.bar(monthly_avg, x="month", y="total_fee_cr", title="Average Monthly Tourism Fee (Cr)", color="total_fee_cr")
st.plotly_chart(fig1)

# Section 2: Peak Tourism Months
st.header("🌟 Peak Tourism Months")
peak_months = get_peak_tourism_months()
fig2 = px.bar(peak_months, x="month", y="total_fee_cr", title="Total Fee by Month", color="total_fee_cr")
st.plotly_chart(fig2)

# Section 3: Yearly Funding vs Tourism
st.header("🔀 Funding vs Tourism Yearly Comparison")
fvsy = get_funding_vs_tourism_by_year()
fig3 = px.line(fvsy, x="year", y=["total_tourism_fee_cr", "total_funding_cr"], markers=True,
               title="Tourism Fee vs Cultural Funding (Cr)")
st.plotly_chart(fig3)

# Section 4: Global Standing
st.header("🌍 India vs Global Tourism Growth")
global_growth = get_india_vs_world_growth()
fig4 = px.line(global_growth, x="YEAR", y=["WORLD_RECEIPTS_GROWTH_RATE", "INDIA_SHARE_GROWTH_RATE"],
               title="India vs World Growth Rate")
st.plotly_chart(fig4)

# Section 5: India's Share in World Tourism
st.header("📈 India’s Global Share & Rank")
share = get_india_global_share_trend()
fig5 = px.line(share, x="YEAR", y="INDIA_SHARE_PCT", title="India’s % Share of World Tourism")
st.plotly_chart(fig5)
