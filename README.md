# barchiver
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com)


The goal of this project is to provide a simple way to generate archival playlists for your music library.

```mermaid
graph TD
    A["Liked Songs"] --> B["2024"]
    A["Liked Songs"] --> C["2023"]
    A["Liked Songs"] --> D["2022"]
    B --> B1["January 2024"]
    B --> B2["February 2024"]
    B --> B3["March 2024"]
    B --> B4["April 2024"]
```

# Usage
```python
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from barchiver.repository import UserRepository
os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"
scope = 'user-library-read, playlist-modify-public, playlist-modify-private, playlist-read-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_repo = UserRepository(sp)

user_repo.create_archival_playlists()
```

## Motivation
I have kept a personal archive of my music for a couple years now, but sometimes I forget to create a playlist. It's nice to be able to go back in your listening history to re-familiarize yourself with the music you were listening to at a certain time. This project is a way to automate that process.
Spotify does allow you to scroll through your liked songs by time, but it often feels like an infinite stream. This aims to better compartmentalize your listening history.

## Roadmap

- [ ] Create a simple CLI
- [x] Work with Spotify API
- [x] Generate playlists based on year/month
- [ ] Create a TUI and a installable package
- [ ] Specify playlist naming/structure
- [ ] Integrate Apple Music
- [ ] Integrate YouTube Music
- [ ] Allow for generated playlist covers
- [ ] ???
- [ ] Profit


## Known Limitations
### Spotify
- The Spotify API currently does not allow for moving a group of playlists into a folder. An operation which you can do on Mobile, Web, Desktop. Why can't the API do this? I don't have a clue.
- The API doesn't allow you to truly `delete` a playlist. Only "unfollowing".

## Personal Goals

For this project I wanted to develop in python in the open. I also wanted to more strictly follow TDD.

### Useful stuff for development

> [!CAUTION]
> Please don't use the ✨**amazing**🤩 Desktop Client when testing. The WebUI is far more responsive.

Scopes
```python
scope = 'user-library-read, playlist-modify-public, playlist-modify-private, playlist-read-private'
```

[Spotify API](https://developer.spotify.com/documentation/web-api/)