"""Respositories for the Barchiver application."""
from spotipy import Spotify
from .models import LikedSong
from loguru import logger


class UserRepository:
    """User repository for the Barchiver application."""

    liked_tracks: list[LikedSong] = []

    def __init__(self, sp: Spotify) -> None:
        """Initialize the user repository."""
        self.sp = sp

    @property
    def get_liked_tracks(self) -> list:
        """Get the liked tracks for the user."""
        if self.liked_tracks:
            return self.liked_tracks
        initial_call = self.sp.current_user_saved_tracks()
        self.liked_tracks.extend(
            [LikedSong(**track) for track in initial_call.get("items")]
        )
        limit = initial_call.get("total")
        logger.warning(
            f"Collecting {limit} liked tracks for the first time. This may take a while. Subsequent operations will be instananeous"
        )
        # ? We can probably parallelize this
        for offset in range(20, limit, 20):
            self.liked_tracks.extend(
                [
                    LikedSong(**track)
                    for track in self.sp.current_user_saved_tracks(offset=offset).get(
                        "items"
                    )
                ]
            )
        return self.liked_tracks
