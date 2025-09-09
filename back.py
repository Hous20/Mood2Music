import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Charger le fichier .env
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise Exception("SPOTIPY_CLIENT_ID ou SPOTIPY_CLIENT_SECRET non trouvé dans .env")

# 🔹 Initialisation Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# Mapping humeur -> genres Spotify
mood_to_genres = {
    "happy": ["pop", "dance"],
    "sad": ["acoustic", "indie"],
    "chill": ["lo-fi", "jazz"],
    "focus": ["classical", "electronic"]
}

# Fonction pour récupérer les morceaux par genre
def get_songs_by_genre(genre, limit=5):
    results = sp.search(q=f'genre:"{genre}"', type='track', limit=limit)
    songs = []
    for item in results['tracks']['items']:
        songs.append({
            "title": item['name'],
            "artist": item['artists'][0]['name'],
            "album": item['album']['name'],
            "popularity": item['popularity'],
            "estimated_streams": item['popularity'] * 10000,  # estimation pour démo
            "genre": genre,
            "image": item['album']['images'][0]['url']
        })
    return songs

# Fonction pour récupérer les morceaux par humeur
def get_songs_by_mood(mood, limit_per_genre=5):
    if mood not in mood_to_genres:
        raise ValueError(f"Humeur inconnue : {mood}")
    
    songs = []
    for genre in mood_to_genres[mood]:
        songs.extend(get_songs_by_genre(genre, limit=limit_per_genre))
    
    # Trier par popularité
    songs.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Limite à 5 morceaux max pour la démo
    return songs[:5]

# Test direct dans le backend
if __name__ == "__main__":
    print("=== Test Backend Mood2Music ===")
    for mood in mood_to_genres.keys():
        print(f"\nMorceaux pour l'humeur : {mood}")
        tracks = get_songs_by_mood(mood)
        for t in tracks:
            print(f"{t['title']} - {t['artist']} | Album: {t['album']} | Popularité: {t['popularity']} | "
                  f"Streams estimés: {t['estimated_streams']} | Genre: {t['genre']} | Image: {t['image']}")
