import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

date = input("Which year do you want to travel to? Type the date in this format YY-MM-DD:" )
URL = f"{os.getenv('URL')}{date}/"
SCRAPPING_HEADER = {"User-Agent": os.getenv("SCRAPPING_HEADER")}
SPOTIPY_CLIENT_ID= os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")

# ================= connecting to spotify ==================
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt",
        username="Paiva4546"
    ))

user_id = sp.current_user()["id"]
print(user_id)

# =========== scrapping songs for the playlist ============
response = requests.get(url=URL, headers=SCRAPPING_HEADER)
website_html = response.text
soup = BeautifulSoup(markup=website_html, features="html.parser")
song_list = soup.select("li ul li h3")
song_names = [songs.getText(strip=True) for songs in song_list]

song_uri = []
for song in song_names:
    result = sp.search(q=f"track:{song}", limit=1, type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipping")

# =========== creating the playlist =============
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Hot 100 Billboard", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)
