"""Global application configs"""
from pydantic_settings import BaseSettings


class BArchiverConfig(BaseSettings):
    """Global application configs"""

    spotify_client_id: str = ""
    spotify_client_secret: str = ""

    playlist_signature: str = "Made with 💓 by barchiver"


BARCHIVER_SETTINGS = BArchiverConfig()
