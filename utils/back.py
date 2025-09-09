import os
import pandas as pd
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from functools import lru_cache

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

# 🔹 Cache pour améliorer les performances
CACHE = {}
CACHE_DURATION = 300  # 5 minutes en secondes

def get_from_cache(key):
    """Récupère une valeur du cache si elle n'est pas expirée"""
    if key in CACHE:
        data, timestamp = CACHE[key]
        if time.time() - timestamp < CACHE_DURATION:
            return data
        else:
            # Cache expiré, le supprimer
            del CACHE[key]
    return None

def save_to_cache(key, data):
    """Sauvegarde une valeur dans le cache avec timestamp"""
    CACHE[key] = (data, time.time())

# Charger le mapping genres -> thèmes depuis le CSV
def load_genre_themes():
    """Charge le mapping genres -> thèmes depuis le fichier CSV"""
    try:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'spotify_genres_themes.csv')
        df = pd.read_csv(csv_path)
        
        # Créer un dictionnaire thème -> liste de genres
        theme_to_genres = {}
        for _, row in df.iterrows():
            theme = row['theme']
            genre = row['genre']
            
            if theme not in theme_to_genres:
                theme_to_genres[theme] = []
            theme_to_genres[theme].append(genre)
        
        return theme_to_genres
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV: {e}")
        # Fallback sur l'ancien mapping
        return {
            "joyeux": ["pop", "dance"],
            "triste": ["acoustic", "indie"],
            "calme": ["lo-fi", "jazz"],
            "énergique": ["electronic", "rock"]
        }

# Charger les données au démarrage
theme_to_genres = load_genre_themes()

# Fonction pour obtenir les thèmes disponibles
def get_available_themes():
    """Retourne la liste des thèmes disponibles"""
    return list(theme_to_genres.keys())

# Fonction pour obtenir les genres d'un thème
def get_genres_for_theme(theme):
    """Retourne les genres associés à un thème"""
    return theme_to_genres.get(theme, [])

# Fonction pour récupérer les morceaux par genre avec cache
def get_songs_by_genre(genre, limit=5):
    """Récupère les morceaux par genre avec mise en cache"""
    cache_key = f"genre_{genre}_{limit}"
    
    # Vérifier le cache d'abord
    cached_result = get_from_cache(cache_key)
    if cached_result is not None:
        return cached_result
    
    try:
        results = sp.search(q=f'genre:"{genre}"', type='track', limit=limit)
        
        if not results or 'tracks' not in results or not results['tracks']:
            save_to_cache(cache_key, [])
            return []
            
        songs = []
        for item in results['tracks']['items']:
            if not item:
                continue
                
            # Vérifier si l'image existe
            image_url = "https://via.placeholder.com/300x300?text=No+Image"
            if item.get('album') and item['album'].get('images') and len(item['album']['images']) > 0:
                image_url = item['album']['images'][0]['url']
                
            songs.append({
                "title": item.get('name', 'Titre inconnu'),
                "artist": item['artists'][0]['name'] if item.get('artists') and len(item['artists']) > 0 else 'Artiste inconnu',
                "album": item['album']['name'] if item.get('album') else 'Album inconnu',
                "popularity": item.get('popularity', 0),
                "popularity_score": item.get('popularity', 0),  # Score Spotify (0-100)
                "genre": genre,
                "image": image_url,
                "spotify_url": item.get('external_urls', {}).get('spotify', ''),
                "preview_url": item.get('preview_url', '')
            })
        
        # Mettre en cache le résultat
        save_to_cache(cache_key, songs)
        return songs
        
    except Exception as e:
        print(f"Erreur lors de la recherche pour le genre {genre}: {e}")
        save_to_cache(cache_key, [])  # Cache le résultat vide aussi
        return []

# Fonction pour récupérer les morceaux par thème avec cache
def get_songs_by_theme(theme, limit_per_genre=2, max_total=10):
    """Récupère les morceaux les plus streamés pour un thème donné avec cache"""
    cache_key = f"theme_{theme}_{limit_per_genre}_{max_total}"
    
    # Vérifier le cache d'abord
    cached_result = get_from_cache(cache_key)
    if cached_result is not None:
        return cached_result
    
    if theme not in theme_to_genres:
        raise ValueError(f"Thème inconnu : {theme}")
    
    all_songs = []
    genres = get_genres_for_theme(theme)
    
    # Limiter le nombre de genres pour éviter trop de requêtes
    selected_genres = genres[:5] if len(genres) > 5 else genres
    
    for genre in selected_genres:
        songs = get_songs_by_genre(genre, limit=limit_per_genre)
        for song in songs:
            song['theme'] = theme  # Ajouter le thème à chaque chanson
        all_songs.extend(songs)
    
    # Trier par popularité (streams estimés)
    all_songs.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Retourner les meilleures chansons
    result = all_songs[:max_total]
    
    # Mettre en cache le résultat
    save_to_cache(cache_key, result)
    return result

# Fonction pour obtenir plus de chansons d'un thème
def get_extended_songs_by_theme(theme, offset=0, limit=20):
    """Récupère plus de chansons pour un thème avec pagination"""
    if theme not in theme_to_genres:
        raise ValueError(f"Thème inconnu : {theme}")
    
    all_songs = []
    genres = get_genres_for_theme(theme)
    
    # Utiliser plus de genres pour les résultats étendus
    songs_per_genre = max(3, limit // len(genres)) if genres else 3
    
    for genre in genres:
        songs = get_songs_by_genre(genre, limit=songs_per_genre)
        for song in songs:
            song['theme'] = theme
        all_songs.extend(songs)
    
    # Trier par popularité
    all_songs.sort(key=lambda x: x['popularity'], reverse=True)
    
    # Appliquer pagination
    start_idx = offset
    end_idx = offset + limit
    
    return all_songs[start_idx:end_idx]

# 🔹 Fonction de recherche intelligente combinée (NOUVELLE)
def smart_search(query, selected_theme=None, limit=20):
    """
    Recherche intelligente qui combine recherche textuelle et filtrage par thème
    
    Args:
        query (str): Terme de recherche (artiste, titre, etc.)
        selected_theme (str): Thème sélectionné pour filtrer les résultats
        limit (int): Nombre de résultats maximum
    
    Returns:
        dict: {
            'results': liste des tracks,
            'total_found': nombre total trouvé,
            'search_info': infos sur la recherche
        }
    """
    cache_key = f"smart_search_{query}_{selected_theme}_{limit}"
    
    # Vérifier le cache
    cached_result = get_from_cache(cache_key)
    if cached_result is not None:
        return cached_result
    
    results = []
    search_info = {}
    
    try:
        # 1. Si pas de terme de recherche, utiliser seulement le thème
        if not query or query.strip() == "":
            if selected_theme:
                results = get_songs_by_theme(selected_theme, limit_per_genre=4, max_total=limit)
                search_info = {
                    'type': 'theme_only',
                    'theme': selected_theme,
                    'message': f"Musiques du thème '{selected_theme}'"
                }
            else:
                # Pas de recherche ni thème - retourner top tracks populaires
                results = get_popular_tracks(limit)
                search_info = {
                    'type': 'popular',
                    'message': "Top musiques populaires"
                }
        
        # 2. Recherche textuelle avec thème optionnel
        else:
            # Recherche de base
            spotify_results = sp.search(q=query, type='track', limit=limit*2)  # Plus pour filtrer
            
            if spotify_results and 'tracks' in spotify_results and spotify_results['tracks']['items']:
                for item in spotify_results['tracks']['items']:
                    if not item:
                        continue
                    
                    # Vérifier si l'image existe
                    image_url = "https://via.placeholder.com/300x300?text=No+Image"
                    if item.get('album') and item['album'].get('images') and len(item['album']['images']) > 0:
                        image_url = item['album']['images'][0]['url']
                    
                    # Déterminer le thème de cette track (basé sur les genres de l'artiste)
                    track_theme = selected_theme or detect_track_theme(item)
                    
                    track_data = {
                        "title": item.get('name', 'Titre inconnu'),
                        "artist": item['artists'][0]['name'] if item.get('artists') and len(item['artists']) > 0 else 'Artiste inconnu',
                        "album": item['album']['name'] if item.get('album') else 'Album inconnu',
                        "popularity": item.get('popularity', 0),
                        "popularity_score": item.get('popularity', 0),
                        "genre": "search_result",
                        "theme": track_theme,
                        "image": image_url,
                        "spotify_url": item.get('external_urls', {}).get('spotify', ''),
                        "preview_url": item.get('preview_url', '')
                    }
                    
                    # Filtrer par thème si sélectionné
                    if not selected_theme or track_theme == selected_theme:
                        results.append(track_data)
                
                # Trier par popularité
                results.sort(key=lambda x: x['popularity'], reverse=True)
                results = results[:limit]
                
                search_info = {
                    'type': 'search_with_theme' if selected_theme else 'search_only',
                    'query': query,
                    'theme': selected_theme,
                    'message': f"Résultats pour '{query}'" + (f" (thème: {selected_theme})" if selected_theme else "")
                }
            
            else:
                # Pas de résultats de recherche, fallback sur le thème
                if selected_theme:
                    results = get_songs_by_theme(selected_theme, limit_per_genre=3, max_total=limit)
                    search_info = {
                        'type': 'fallback_theme',
                        'query': query,
                        'theme': selected_theme,
                        'message': f"Aucun résultat pour '{query}', voici des suggestions du thème '{selected_theme}'"
                    }
                else:
                    results = []
                    search_info = {
                        'type': 'no_results',
                        'query': query,
                        'message': f"Aucun résultat trouvé pour '{query}'"
                    }
    
    except Exception as e:
        print(f"Erreur dans smart_search: {e}")
        results = []
        search_info = {
            'type': 'error',
            'message': "Erreur lors de la recherche"
        }
    
    # Préparer le résultat final
    final_result = {
        'results': results,
        'total_found': len(results),
        'search_info': search_info
    }
    
    # Mettre en cache
    save_to_cache(cache_key, final_result)
    return final_result

def detect_track_theme(track_item):
    """Essaie de deviner le thème d'une track basé sur ses caractéristiques"""
    # Pour l'instant, retourner un thème par défaut
    # On pourrait analyser les genres de l'artiste ou la popularité
    popularity = track_item.get('popularity', 0)
    
    if popularity > 80:
        return 'joyeux'
    elif popularity > 60:
        return 'énergique'
    elif popularity > 40:
        return 'calme'
    else:
        return 'mélancolique'

def get_popular_tracks(limit=10):
    """Récupère des tracks populaires générales"""
    cache_key = f"popular_tracks_{limit}"
    
    cached_result = get_from_cache(cache_key)
    if cached_result is not None:
        return cached_result
    
    try:
        # Rechercher des tracks populaires globales
        results = sp.search(q='year:2024', type='track', limit=limit)
        
        tracks = []
        if results and 'tracks' in results:
            for item in results['tracks']['items']:
                if not item:
                    continue
                    
                image_url = "https://via.placeholder.com/300x300?text=No+Image"
                if item.get('album') and item['album'].get('images') and len(item['album']['images']) > 0:
                    image_url = item['album']['images'][0]['url']
                
                tracks.append({
                    "title": item.get('name', 'Titre inconnu'),
                    "artist": item['artists'][0]['name'] if item.get('artists') and len(item['artists']) > 0 else 'Artiste inconnu',
                    "album": item['album']['name'] if item.get('album') else 'Album inconnu',
                    "popularity": item.get('popularity', 0),
                    "popularity_score": item.get('popularity', 0),
                    "genre": "popular",
                    "theme": detect_track_theme(item),
                    "image": image_url,
                    "spotify_url": item.get('external_urls', {}).get('spotify', ''),
                    "preview_url": item.get('preview_url', '')
                })
        
        save_to_cache(cache_key, tracks)
        return tracks
        
    except Exception as e:
        print(f"Erreur get_popular_tracks: {e}")
        return []

# Fonction de recherche intelligente avec résultats multiples
def search_spotify(query, search_type="track", limit=10):
    """
    Fonction de recherche Spotify qui garde la logique d'affichage des résultats possibles
    
    Args:
        query (str): Terme de recherche (artiste, titre, album)
        search_type (str): Type de recherche - "track", "artist", "album"
        limit (int): Nombre de résultats à retourner
    
    Returns:
        list: Liste des résultats formatés
    """
    try:
        # Recherche sur Spotify
        results = sp.search(q=query, type=search_type, limit=limit)
        
        if not results:
            return []
        
        songs = []
        if search_type == "track" and 'tracks' in results and results['tracks']:
            for item in results['tracks']['items']:
                if not item:
                    continue
                    
                # Vérifier si l'image existe
                image_url = "https://via.placeholder.com/300x300?text=No+Image"
                if item.get('album') and item['album'].get('images') and len(item['album']['images']) > 0:
                    image_url = item['album']['images'][0]['url']
                
                songs.append({
                    "title": item.get('name', 'Titre inconnu'),
                    "artist": item['artists'][0]['name'] if item.get('artists') and len(item['artists']) > 0 else 'Artiste inconnu',
                    "album": item['album']['name'] if item.get('album') else 'Album inconnu',
                    "popularity": item.get('popularity', 0),
                    "popularity_score": item.get('popularity', 0),  # Score Spotify (0-100)
                    "genre": "search_result",  # Marqueur pour les résultats de recherche
                    "image": image_url,
                    "spotify_url": item.get('external_urls', {}).get('spotify', ''),
                    "preview_url": item.get('preview_url', '')
                })
        
        elif search_type == "artist" and 'artists' in results and results['artists']:
            # Si on cherche un artiste, on récupère ses top tracks
            for artist in results['artists']['items']:
                if not artist:
                    continue
                    
                try:
                    artist_tracks = sp.artist_top_tracks(artist['id'])
                    if artist_tracks and 'tracks' in artist_tracks:
                        for track in artist_tracks['tracks'][:5]:  # Top 5 de l'artiste
                            if not track:
                                continue
                                
                            image_url = "https://via.placeholder.com/300x300?text=No+Image"
                            if track.get('album') and track['album'].get('images') and len(track['album']['images']) > 0:
                                image_url = track['album']['images'][0]['url']
                            
                            songs.append({
                                "title": track.get('name', 'Titre inconnu'),
                                "artist": track['artists'][0]['name'] if track.get('artists') and len(track['artists']) > 0 else 'Artiste inconnu',
                                "album": track['album']['name'] if track.get('album') else 'Album inconnu',
                                "popularity": track.get('popularity', 0),
                                "popularity_score": track.get('popularity', 0),  # Score Spotify (0-100)
                                "genre": f"artist:{artist.get('name', 'Artiste inconnu')}",
                                "image": image_url,
                                "spotify_url": track.get('external_urls', {}).get('spotify', ''),
                                "preview_url": track.get('preview_url', '')
                            })
                except Exception as artist_error:
                    print(f"Erreur lors de la récupération des tracks de l'artiste {artist.get('name', 'Inconnu')}: {artist_error}")
                    continue
        
        # Trier par popularité pour garder la logique
        songs.sort(key=lambda x: x['popularity'], reverse=True)
        
        return songs
        
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        return []

# Fonction pour obtenir les suggestions de recherche
def get_search_suggestions(query, limit=5):
    """
    Obtenir des suggestions de recherche basées sur la requête partielle
    """
    if len(query) < 2:
        return []
    
    try:
        # Recherche d'artistes pour suggestions
        artist_results = sp.search(q=query, type='artist', limit=limit)
        # Recherche de tracks pour suggestions
        track_results = sp.search(q=query, type='track', limit=limit)
        
        suggestions = []
        
        # Ajouter les artistes
        if artist_results and 'artists' in artist_results and artist_results['artists']:
            for artist in artist_results['artists']['items']:
                if artist and artist.get('name'):
                    suggestions.append({
                        "type": "artist",
                        "name": artist['name'],
                        "suggestion": artist['name']
                    })
        
        # Ajouter les titres populaires
        if track_results and 'tracks' in track_results and track_results['tracks']:
            for track in track_results['tracks']['items']:
                if track and track.get('name'):
                    artist_name = track['artists'][0]['name'] if track.get('artists') and len(track['artists']) > 0 else 'Artiste inconnu'
                    suggestions.append({
                        "type": "track",
                        "name": f"{track['name']} - {artist_name}",
                        "suggestion": track['name']
                    })
        
        return suggestions[:limit]
        
    except Exception as e:
        print(f"Erreur lors des suggestions : {e}")
        return []

# Test direct dans le backend
if __name__ == "__main__":
    print("=== Test Backend Mood2Music avec Thèmes Spotify ===")
    
    # Afficher les thèmes disponibles
    print(f"\n=== Thèmes disponibles ({len(theme_to_genres)}) ===")
    for theme, genres in list(theme_to_genres.items())[:10]:  # Afficher les 10 premiers
        print(f"{theme}: {len(genres)} genres - Exemples: {', '.join(genres[:3])}")
    
    # Test de récupération d'un seul morceau pour vérifier tous les champs
    print("\n=== Test détaillé d'un morceau ===")
    test_tracks = get_songs_by_genre("pop", limit=1)
    if test_tracks:
        track = test_tracks[0]
        print(f"Titre: {track['title']}")
        print(f"Artiste: {track['artist']}")
        print(f"Album: {track['album']}")
        print(f"Popularité: {track['popularity']}")
        print(f"Lien Spotify: {track.get('spotify_url', 'NON DISPONIBLE')}")
        print(f"URL preview: {track.get('preview_url', 'NON DISPONIBLE')}")
        print(f"Image: {track['image']}")
    
    # Test par thème
    print("\n=== Test par thème (premiers thèmes) ===")
    test_themes = ['joyeux', 'énergique', 'calme', 'triste']
    for theme in test_themes:
        if theme in theme_to_genres:
            print(f"\nMorceaux pour le thème : {theme}")
            try:
                tracks = get_songs_by_theme(theme, limit_per_genre=1, max_total=3)
                for t in tracks:
                    spotify_link = t.get('spotify_url', 'NON DISPONIBLE')
                    print(f"  - {t['title']} - {t['artist']} | Popularité: {t['popularity']} | Spotify: {spotify_link}")
            except Exception as e:
                print(f"  Erreur: {e}")
        else:
            print(f"\nThème '{theme}' non trouvé dans les données")
