# streamlit_app.py
import streamlit as st
from PIL import Image

st.set_page_config(page_title="India’s Hidden Culture", layout="wide")

st.sidebar.title("📍 Navigation")
st.sidebar.markdown("Choose a page from below:")

# Streamlit uses pages/ directory automatically, no routing needed
st.markdown("# 🇮🇳 India's Hidden Culture & Tourism")
st.markdown("Use the sidebar to explore tourism trends, cultural funding, and more.")
