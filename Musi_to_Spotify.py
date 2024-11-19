import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Spotify API credentials
SPOTIFY_CLIENT_ID = "Replace with Client ID"
SPOTIFY_CLIENT_SECRET = "Replace with Client Secret"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-public"
))

def fetch_playlist():
    """Extracts songs from a Musi playlist."""
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Open the Musi playlist URL
    url = "https://feelthemusi.com/playlist/z1enh9"  # Replace with the actual Musi playlist link
    driver.get(url)

    try:
        # Wait until the songs are loaded
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'track')))
        html = driver.page_source
    except Exception as e:
        print(f"Error loading Musi playlist: {e}")
        driver.quit()
        return []

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    songs = []
    for track in soup.find_all('a', class_='track'):
        title_div = track.find('div', class_='video_title')
        artist_div = track.find('div', class_='video_artist')
        title = title_div.text.strip() if title_div else "Unknown Title"
        artist = artist_div.text.strip() if artist_div else "Unknown Artist"
        songs.append((title, artist))
    
    driver.quit()
    return songs

def search_spotify_track(title, artist):
    """Search for a track on Spotify by title and artist."""
    query = f"{title} {artist}"
    results = sp.search(q=query, type="track", limit=1)
    tracks = results.get("tracks", {}).get("items", [])
    if tracks:
        return tracks[0]["id"]  # Return the Spotify track ID
    return None

def create_spotify_playlist(playlist_name, description="Converted from Musi"):
    """Create a new Spotify playlist."""
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=description)
    return playlist["id"]

def add_tracks_to_playlist(playlist_id, track_ids):
    """Add tracks to a Spotify playlist in chunks of 100."""
    chunk_size = 100  # Spotify's limit for adding tracks per request
    for i in range(0, len(track_ids), chunk_size):
        chunk = track_ids[i:i + chunk_size]
        sp.playlist_add_items(playlist_id, chunk)

def convert_musi_to_spotify(musi_playlist_url, spotify_playlist_name):
    """Convert a Musi playlist to a Spotify playlist."""
    # Fetch the Musi playlist
    print("Fetching Musi playlist...")
    musi_songs = fetch_playlist()
    if not musi_songs:
        print("No songs found in the Musi playlist.")
        return

    print(f"Found {len(musi_songs)} songs in the Musi playlist.")

    # Create a new Spotify playlist
    print("Creating a new Spotify playlist...")
    spotify_playlist_id = create_spotify_playlist(spotify_playlist_name)
    print(f"Spotify playlist '{spotify_playlist_name}' created.")

    # Search for each song on Spotify
    spotify_track_ids = []
    missing_songs = []
    for title, artist in musi_songs:
        print(f"Searching for '{title}' by {artist}...")
        track_id = search_spotify_track(title, artist)
        if track_id:
            spotify_track_ids.append(track_id)
        else:
            print(f"Song '{title}' by {artist} not found on Spotify.")
            missing_songs.append((title, artist))

    # Add found tracks to the Spotify playlist
    if spotify_track_ids:
        print("Adding songs to the Spotify playlist...")
        add_tracks_to_playlist(spotify_playlist_id, spotify_track_ids)
        print(f"Added {len(spotify_track_ids)} songs to the Spotify playlist.")
    else:
        print("No songs were found on Spotify to add to the playlist.")

    # Print missing songs
    if missing_songs:
        print("\nThe following songs could not be found on Spotify:")
        for title, artist in missing_songs:
            print(f"- {title} by {artist}")

# Main
if __name__ == "__main__":
    # URL of the Musi playlist and the desired Spotify playlist name
    musi_playlist_url = "https://feelthemusi.com/playlist/"  # Replace with your actual Musi URL
    spotify_playlist_name = "Musi to Spotify Playlist"  # Desired name for the Spotify playlist

    # Convert the playlist
    convert_musi_to_spotify(musi_playlist_url, spotify_playlist_name)