import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Music2Mood Home",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Importer et exécuter la landing page
exec(open('pages/landing_page.py').read())