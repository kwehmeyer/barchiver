import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

os.environ["SPOTIPY_CLIENT_ID"] = "4f779023cc4c4e1f9b7e04623208d8c9"
os.environ["SPOTIPY_CLIENT_SECRET"] = "2a989d74a667429e814ea1048e61e934"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"
os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
