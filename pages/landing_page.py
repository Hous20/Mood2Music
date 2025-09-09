import streamlit as st
import pandas as pd
import sys
import os

# Ajouter le répertoire parent au path pour importer back.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from utils.back import (get_songs_by_theme, get_extended_songs_by_theme, get_songs_by_genre, 
                           theme_to_genres, search_spotify, get_available_themes, smart_search)
    spotify_connection_ok = True
except ImportError as e:
    st.error(f"❌ Impossible d'importer le module back.py: {e}")
    st.error("Vérifiez que le fichier .env existe avec vos credentials Spotify")
    spotify_connection_ok = False
except Exception as e:
    st.error(f"❌ Erreur de connexion Spotify: {e}")
    st.error("Vérifiez vos credentials dans le fichier .env")
    spotify_connection_ok = False

# Inclure Ionicons dans l'application
st.markdown("""
<script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
""", unsafe_allow_html=True)

st.markdown('<h1><ion-icon name="musical-notes"></ion-icon> Mood2Music</h1>', unsafe_allow_html=True)
st.markdown("")  # Espace après le titre

# Vérification de la connexion Spotify
if not spotify_connection_ok:
    st.error("❌ Problème de connexion à Spotify")
    st.info("💡 Pour utiliser l'application, vous devez configurer vos credentials Spotify dans le fichier .env")
    st.stop()

# Charger les données depuis Spotify (pour le TOP 10)
@st.cache_data(ttl=300)  # Cache pendant 5 minutes
def load_spotify_top_tracks():
    """Charge les pistes populaires depuis différents genres"""
    if not spotify_connection_ok:
        return []
    
    try:
        # Récupérer plusieurs genres populaires
        popular_genres = ["pop", "rock", "hip hop", "electronic", "jazz"]
        all_tracks = []
        
        for genre in popular_genres:
            results = search_spotify(f"genre:{genre}", "track", 4)  # 4 par genre
            all_tracks.extend(results)
        
        # Trier par popularité et retourner les top tracks
        all_tracks.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        return all_tracks[:15]  # Top 15 pour avoir du choix
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des pistes populaires: {e}")
        return []

st.markdown("---")

# 🔹 INTERFACE UNIFIÉE : RECHERCHE + THÈME
st.markdown('<h3><ion-icon name="search"></ion-icon> Recherche intelligente</h3>', unsafe_allow_html=True)

# Charger les thèmes disponibles
try:
    available_themes = get_available_themes()
    available_themes_filtered = available_themes[:8] if len(available_themes) > 8 else available_themes
    
    if len(available_themes_filtered) < 8:
        other_themes = [t for t in available_themes if t not in available_themes_filtered][:8-len(available_themes_filtered)]
        available_themes_filtered.extend(other_themes)
except:
    available_themes_filtered = ["joyeux", "triste", "calme", "énergique"]

# Interface unifiée : Recherche + Thème + Limite de résultats
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    # Option "Tous les thèmes" en premier
    theme_options = ["Tous les thèmes"] + available_themes_filtered
    selected_theme_raw = st.selectbox("🎭 Thème musical", theme_options, key="theme_selector")
    selected_theme = None if selected_theme_raw == "Tous les thèmes" else selected_theme_raw
with col2:
    search_query = st.text_input("🔍 Rechercher", "", 
                                help="Recherche par artiste, titre... Combiné avec le thème sélectionné")
with col3:
    results_limit = st.selectbox("Résultats", [10, 20, 50], index=0, key="results_limit")

st.markdown("")  # Espace après la sélection

# 🔹 RECHERCHE INTELLIGENTE UNIFIÉE
if spotify_connection_ok:
    try:
        # Utiliser smart_search qui combine recherche textuelle + thème
        search_result = smart_search(
            query=search_query.strip() if search_query else "",
            selected_theme=selected_theme,
            limit=results_limit
        )
        
        tracks = search_result['results']
        search_info = search_result['search_info']
        
        # Afficher le message informatif
        if search_info.get('message'):
            if search_info['type'] == 'no_results':
                st.warning(search_info['message'])
            elif search_info['type'] == 'fallback_theme':
                st.info(search_info['message'])
            elif search_info['type'] == 'popular':
                st.info("🔥 " + search_info['message'])
            else:
                st.success("🎵 " + search_info['message'])
        
        # Afficher les résultats si il y en a
        if tracks:
            st.markdown(f"**🎵 {len(tracks)} résultats trouvés**")
            st.markdown("")  # Espace
            
            # En-têtes des colonnes
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1.2, 1.3, 1])
            with col1:
                st.markdown("**<ion-icon name='musical-notes'></ion-icon> Cover**", unsafe_allow_html=True)
            with col2:
                st.markdown("**<ion-icon name='happy'></ion-icon> Title | <ion-icon name='library'></ion-icon> Artist**", unsafe_allow_html=True)
            with col3:
                st.markdown("**<ion-icon name='mic'></ion-icon> Album**", unsafe_allow_html=True)
            with col4:
                st.markdown("**<ion-icon name='headset'></ion-icon> Popularity**", unsafe_allow_html=True)
            with col5:
                st.markdown("**<ion-icon name='analytics-outline'></ion-icon> Score Spotify**", unsafe_allow_html=True)
            with col6:
                st.markdown("**<ion-icon name='link'></ion-icon> Spotify**", unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Afficher chaque track
            for track in tracks:
                col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1.2, 1.3, 1])
                with col1:
                    st.image(track['image'], width=60)
                with col2:
                    # Afficher le thème en plus si disponible
                    theme_badge = f" | 🎭 {track.get('theme', 'N/A')}" if track.get('theme') else ""
                    st.write(f"**{track['title']}** | {track['artist']}{theme_badge}")
                with col3:
                    st.markdown(f"<ion-icon name='mic'></ion-icon> {track['album']}", unsafe_allow_html=True)
                with col4:
                    st.markdown(f"<ion-icon name='headset'></ion-icon> {track['popularity']}/100", unsafe_allow_html=True)
                with col5:
                    popularity_score = track.get('popularity_score', track.get('popularity', 0))
                    st.markdown(f"<ion-icon name='analytics-outline'></ion-icon> {popularity_score}/100", unsafe_allow_html=True)
                with col6:
                    if track.get('spotify_url'):
                        st.markdown(f'<a href="{track["spotify_url"]}" target="_blank"><ion-icon name="musical-notes"></ion-icon> Écouter</a>', unsafe_allow_html=True)
                    else:
                        st.markdown("❌ Indisponible")
        else:
            st.warning("😔 Aucun résultat trouvé. Essayez avec un autre thème ou terme de recherche.")
    
    except Exception as e:
        st.error(f"❌ Erreur lors de la recherche: {e}")
        st.info("💡 Essayez de changer le thème ou simplifier votre recherche.")
else:
    st.error("❌ Connexion Spotify indisponible")

# 🔹 SECTION TOP 10 POPULAIRES (Affichée quand pas de recherche)
if not search_query and not selected_theme:
    st.markdown("---")
    st.markdown('<h3><ion-icon name="trophy"></ion-icon> Top 10 des pistes populaires</h3>', unsafe_allow_html=True)
    st.markdown("")  # Espace après le sous-titre
    
    spotify_tracks = load_spotify_top_tracks()[:10]  # Limiter à 10 pistes
    
    if spotify_tracks:
        # En-têtes pour la section Top 10
        col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1.2, 1.3, 1])
        
        with col1:
            st.markdown("**<ion-icon name='musical-notes'></ion-icon> Cover**", unsafe_allow_html=True)
        with col2:
            st.markdown("**<ion-icon name='happy'></ion-icon> Title | <ion-icon name='library'></ion-icon> Artist**", unsafe_allow_html=True)
        with col3:
            st.markdown("**<ion-icon name='mic'></ion-icon> Album**", unsafe_allow_html=True)
        with col4:
            st.markdown("**<ion-icon name='headset'></ion-icon> Popularity**", unsafe_allow_html=True)
        with col5:
            st.markdown("**<ion-icon name='analytics-outline'></ion-icon> Score Spotify**", unsafe_allow_html=True)
        with col6:
            st.markdown("**<ion-icon name='link'></ion-icon> Spotify**", unsafe_allow_html=True)
        
        st.markdown("---")  # Ligne de séparation
        
        # Afficher les pistes populaires depuis Spotify
        for track in spotify_tracks:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 1.2, 1.3, 1])
            with col1:
                st.image(track['image'], width=60)
            with col2:
                st.write(f"**{track['title']}** | {track['artist']}")
            with col3:
                st.markdown(f"<ion-icon name='mic'></ion-icon> {track['album']}", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<ion-icon name='headset'></ion-icon> {track['popularity']}/100", unsafe_allow_html=True)
            with col5:
                popularity_score = track.get('popularity_score', track.get('popularity', 0))
                st.markdown(f"<ion-icon name='analytics-outline'></ion-icon> {popularity_score}/100", unsafe_allow_html=True)
            with col6:
                if track.get('spotify_url'):
                    st.markdown(f'<a href="{track["spotify_url"]}" target="_blank"><ion-icon name="musical-notes"></ion-icon> Écouter</a>', unsafe_allow_html=True)
                else:
                    st.markdown("❌ Indisponible")
    else:
        st.error("❌ Erreur lors du chargement des pistes populaires.")

# Footer
st.markdown("---")
st.markdown("Powered by Spotify API 🎵")
