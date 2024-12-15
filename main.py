import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ssl

# SSL-Konfiguration zur Fehlerbehebung
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# Spotify API-Zugangsdaten aus Umgebungsvariablen mit Fehlerbehandlung
CLIENT_ID = os.getenv('CLIENT_ID', '05475600cfe0422eb2b482e2300941e9')
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '8581b74000da4e6eb80c39314ea95ead')
REDIRECT_URI = 'https://mynametouse.github.io/spotify-app/callback'

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError("CLIENT_ID und CLIENT_SECRET müssen als Umgebungsvariablen gesetzt sein.")

# Authentifizierung mit Autorisierungs-Code-Flow
try:
    print("Authentifizierung wird gestartet...")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-read-private playlist-modify-public",
        open_browser=False
    ))
    print("Authentifizierung erfolgreich!")
except spotipy.exceptions.SpotifyException as e:
    raise RuntimeError(f"Fehler bei der Authentifizierung: {e}")
except Exception as e:
    raise RuntimeError(f"Allgemeiner Fehler bei der Authentifizierung: {e}")

# Playlist-Erstellungsfunktion
def create_christmas_playlist(user_id, name="Weihnachtliche Musik ohne Piano", description="Entspannte Weihnachtsmusik ohne Klavierstücke"):
    try:
        print(f"Erstelle Playlist '{name}' für Benutzer {user_id}...")
        playlist = sp.user_playlist_create(user_id, name, public=True, description=description)
        playlist_id = playlist['id']

        search_query = "Christmas OR Holiday OR Weihnachten"
        print(f"Suche nach Songs mit dem Suchbegriff: {search_query}")

        results = sp.search(q=search_query, type="track", limit=50)
        print("Songsuche abgeschlossen.")

        tracks = [
            track['uri'] for track in results['tracks']['items']
            if 'piano' not in track['name'].lower() and
               any(genre in track['album']['name'].lower() for genre in ['instrumental', 'classic', 'elektro'])
        ]

        if tracks:
            sp.playlist_add_items(playlist_id, tracks)
            print(f"Füge {len(tracks)} Titel zur Playlist hinzu...")
            print(f"Öffentliche Playlist '{name}' wurde erfolgreich erstellt!")
        else:
            print("Keine passenden Titel gefunden.")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API-Fehler bei der Playlist-Erstellung: {e}")
        raise RuntimeError(f"Fehler bei der Playlist-Erstellung: {e}")
    except IOError as io_err:
        print("Netzwerkproblem erkannt. Bitte überprüfen Sie Ihre Internetverbindung und versuchen Sie es erneut.")
        raise RuntimeError(f"I/O-Fehler bei der Playlist-Erstellung: {io_err}")
    except Exception as e:
        raise RuntimeError(f"Allgemeiner Fehler bei der Playlist-Erstellung: {e}")

try:
    print("Benutzerinformationen werden abgerufen...")
    user_id = sp.me()['id']
    print(f"Benutzer-ID abgerufen: {user_id}")
    create_christmas_playlist(user_id)
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify API-Fehler: {e}")
    raise RuntimeError(f"Fehler bei der Benutzer-Authentifizierung: {e}")
except IOError as io_err:
    print("Netzwerkproblem erkannt. Bitte stellen Sie sicher, dass eine Internetverbindung besteht.")
    raise RuntimeError(f"I/O-Fehler: {io_err}")
except Exception as e:
    raise RuntimeError(f"Allgemeiner Fehler: {e}")
