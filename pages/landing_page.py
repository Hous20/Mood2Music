import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Music2Mood Home",
    page_icon=":guardsman:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inclure Ionicons dans l'application
st.markdown("""
<script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
""", unsafe_allow_html=True)

st.markdown('<h1><ion-icon name="musical-notes"></ion-icon> Mood2Music</h1>', unsafe_allow_html=True)
st.markdown("")  # Espace après le titre

# Barre de recherche
search_query = st.text_input("🔍 Rechercher une musique ou un artiste", "")
st.markdown("")  # Espace après la recherche

# Fonction de recherche
def search_music(df, query):
    if not query:
        return df
    query = query.lower()
    mask = (
        df['Thème'].str.lower().str.contains(query, na=False) |
        df['Genre'].str.lower().str.contains(query, na=False) |
        df['Artiste'].str.lower().str.contains(query, na=False)
    )
    return df[mask]

st.markdown("---")

# Filtres sous forme de colonnes avec images
st.markdown('<h3><ion-icon name="musical-notes"></ion-icon> Discover the music for your mood</h3>', unsafe_allow_html=True)
st.markdown("")  # Espace après le sous-titre

# Charger les données du CSV
@st.cache_data
def load_music_data():
    df = pd.read_csv("data/Music_theme.csv")
    # Nettoyer les espaces dans les noms de colonnes
    df.columns = df.columns.str.strip()
    # Renommer la colonne problématique
    df.columns = ['id', 'Thème', 'Genre', 'Artiste', 'Nb_écoutes']
    return df

music_df = load_music_data()

# Appliquer la recherche si une requête est saisie
if search_query:
    st.markdown(f'<h3><ion-icon name="search"></ion-icon> Résultats pour: \'{search_query}\'</h3>', unsafe_allow_html=True)
    st.markdown("")  # Espace
    search_results = search_music(music_df, search_query)
    
    if len(search_results) > 0:
        # En-têtes des colonnes pour les résultats de recherche
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.markdown("**<ion-icon name='musical-notes'></ion-icon> Cover**", unsafe_allow_html=True)
        with col2:
            st.markdown("**<ion-icon name='happy'></ion-icon> Theme | <ion-icon name='library'></ion-icon> Genre**", unsafe_allow_html=True)
        with col3:
            st.markdown("**<ion-icon name='mic'></ion-icon> Artist**", unsafe_allow_html=True)
        with col4:
            st.markdown("**<ion-icon name='headset'></ion-icon> Listens**", unsafe_allow_html=True)
        
        st.markdown("---")
        
        image_path = "images.png"
        for _, row in search_results.iterrows():
            col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
            with col1:
                st.image(image_path, width=60)
            with col2:
                st.write(f"**{row['Thème']}** | {row['Genre']}")
            with col3:
                st.markdown(f"<ion-icon name='mic'></ion-icon> {row['Artiste']}", unsafe_allow_html=True)
            with col4:
                st.markdown(f"<ion-icon name='headset'></ion-icon> {row['Nb_écoutes']:,} écoutes", unsafe_allow_html=True)
    else:
        st.markdown("<ion-icon name='close-circle'></ion-icon> Aucun résultat trouvé pour cette recherche.", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("")  # Espace supplémentaire

# Section des plus populaires
st.markdown('<h3><ion-icon name="flame"></ion-icon> Top 10 - Most Popular</h3>', unsafe_allow_html=True)
st.markdown("")  # Espace

# En-têtes des colonnes
col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
with col1:
    st.markdown("**<ion-icon name='musical-notes'></ion-icon> Cover**", unsafe_allow_html=True)
with col2:
    st.markdown("**<ion-icon name='happy'></ion-icon> Theme | <ion-icon name='library'></ion-icon> Genre**", unsafe_allow_html=True)
with col3:
    st.markdown("**<ion-icon name='mic'></ion-icon> Artist**", unsafe_allow_html=True)
with col4:
    st.markdown("**<ion-icon name='headset'></ion-icon> Listens**", unsafe_allow_html=True)

st.markdown("---")  # Ligne de séparation

image_path = "images.png"

# Trier par nombre d'écoutes (les plus écoutés en premier)
top_tracks = music_df.nlargest(10, 'Nb_écoutes')

for _, row in top_tracks.iterrows():
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    with col1:
        st.image(image_path, width=60)
    with col2:
        st.write(f"**{row['Thème']}** | {row['Genre']}")
    with col3:
        st.markdown(f"<ion-icon name='mic'></ion-icon> {row['Artiste']}", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<ion-icon name='headset'></ion-icon> {row['Nb_écoutes']:,} écoutes", unsafe_allow_html=True)

st.markdown("")  # Espace après le Top 10

# Afficher les thèmes disponibles
st.markdown("---")
st.markdown("")  # Espace
st.markdown('<h3><ion-icon name="happy"></ion-icon> Browse by Theme</h3>', unsafe_allow_html=True)
st.markdown("")  # Espace après le sous-titre
themes = music_df['Thème'].unique()
selected_theme = st.selectbox("Choose your mood", themes)
st.markdown("")  # Espace après le selectbox

if selected_theme:
    filtered_data = music_df[music_df['Thème'] == selected_theme]
    st.markdown(f"**Genres for {selected_theme} mood:**")
    st.markdown("")  # Espace
    
    # En-têtes pour la section thème
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    with col1:
        st.markdown("**<ion-icon name='musical-notes'></ion-icon> Cover**", unsafe_allow_html=True)
    with col2:
        st.markdown("**<ion-icon name='library'></ion-icon> Genre**", unsafe_allow_html=True)
    with col3:
        st.markdown("**<ion-icon name='mic'></ion-icon> Artist**", unsafe_allow_html=True)
    with col4:
        st.markdown("**<ion-icon name='headset'></ion-icon> Listens**", unsafe_allow_html=True)
    
    st.markdown("---")  # Ligne de séparation
    
    # Afficher sous forme de cartes
    for _, genre_row in filtered_data.iterrows():
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.image(image_path, width=50)
        with col2:
            st.write(f"**{genre_row['Genre']}**")
        with col3:
            st.markdown(f"<ion-icon name='mic'></ion-icon> {genre_row['Artiste']}", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<ion-icon name='headset'></ion-icon> {genre_row['Nb_écoutes']:,}", unsafe_allow_html=True)

st.markdown("")  # Espace final
st.markdown("---")
if search_query:
    st.write(f"Recherche active : **{search_query}**")
else:
    st.write("Utilisez la barre de recherche pour trouver de la musique par thème, genre ou artiste")