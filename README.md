# Mood2Music
Appli to recommend music based on mood
🎶 Plan de projet “Mood2Music” (4 heures)
🔹 Étape 1 : Définir le flux utilisateur (15 min)

👉 Votre démo doit montrer :

L’utilisateur choisit son humeur (happy, sad, chill, focus).

L’app affiche quelques morceaux recommandés depuis Spotify (titres + artistes + images).

💡 Pas besoin d’authentification utilisateur complexe → juste un mapping humeur → genres → Spotify.

🔹 Étape 2 : Répartition des rôles (4 personnes)

👤 Backend / Spotify API (1 personne)

Utiliser Spotipy (SDK Spotify en Python).

Faire une fonction get_songs_by_genre(genre) qui renvoie 5 morceaux (titre, artiste, jaquette).

Si temps, exposer un endpoint FastAPI /mood/{mood}.

Sinon, Streamlit peut directement appeler la fonction Python (plus rapide).

👤 Frontend Streamlit (1 personne)

Construire une page avec 4 boutons (😊 😢 😎 🎉).

Quand on clique → appelle la fonction backend et affiche les morceaux.

👤 Data / Mapping (1 personne)

Créer un petit dictionnaire Python :

moods = {
    "happy": ["pop", "dance"],
    "sad": ["acoustic", "indie"],
    "chill": ["lo-fi", "jazz"],
    "focus": ["classical", "electronic"]
}


Sert à traduire humeur → genres Spotify.

👤 Intégration & Pitch (1 personne)

Branche frontend + backend.

Préparez la démo (2 scénarios).

Écrit les 2–3 slides de présentation (problème → solution → démo → impact).

🔹 Étape 3 : Plan technique rapide

Installer dépendances (10 min)

pip install spotipy streamlit


Créer un compte développeur Spotify

Obtenir client_id + client_secret

Les mettre dans un fichier .env

Backend minimal (Spotipy)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
))

def get_songs_by_genre(genre):
    results = sp.search(q=f'genre:{genre}', type='track', limit=5)
    songs = []
    for item in results['tracks']['items']:
        songs.append({
            "title": item['name'],
            "artist": item['artists'][0]['name'],
            "image": item['album']['images'][0]['url']
        })
    return songs


Frontend Streamlit (simple UI)

import streamlit as st

moods = {
    "😊 Happy": "pop",
    "😢 Sad": "acoustic",
    "😎 Chill": "lo-fi",
    "🎯 Focus": "classical"
}

st.title("🎶 Mood2Music")

choice = st.radio("Choisis ton humeur :", list(moods.keys()))

if st.button("Recommander"):
    songs = get_songs_by_genre(moods[choice])
    for s in songs:
        st.image(s["image"], width=100)
        st.write(f"{s['title']}** - {s['artist']}")


👉 Avec ça, en 3 heures max, vous avez une démo qui marche.

🔹 Étape 4 : Démo finale (dernière heure)

Lancer l’app Streamlit :

streamlit run app.py


Montrer : je choisis 😊 → suggestions de pop.

Montrer : je choisis 😎 → suggestions de lo-fi.

Pitch rapide (problème → solution → démo → impact).