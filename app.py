import streamlit as st
import sys
import os

# Configuration de la page (une seule fois)
if "page_configured" not in st.session_state:
    st.set_page_config(
        page_title="Mood2Music - Ressentez la musique",
        page_icon="🎵",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.session_state.page_configured = True

# Ajouter le répertoire des pages au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'pages'))

# Importer et exécuter la page d'accueil
try:
    import home
except ImportError as e:
    st.error(f"Erreur d'import: {e}")
    st.info("Vérifiez que le fichier home.py existe dans le dossier pages/")
    st.info("Vérifiez que le fichier pages/home.py existe")