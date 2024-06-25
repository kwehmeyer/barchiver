"""Respositories for the Barchiver application."""
from spotipy import Spotify
from .models import LikedSong
from loguru import logger
import pandas as pd


class UserRepository:
    """User repository for the Barchiver application."""

    _liked_tracks: list[LikedSong] = []

    def __init__(self, sp: Spotify) -> None:
        """Initialize the user repository."""
        self.sp = sp

    @property
    def get_liked_tracks(self) -> list:
        """Get the liked tracks for the user."""
        if self._liked_tracks:
            return self._liked_tracks
        initial_call = self.sp.current_user_saved_tracks()
        self._liked_tracks.extend(
            [LikedSong(**track) for track in initial_call.get("items")]
        )
        limit = initial_call.get("total")
        logger.warning(
            f"Collecting {limit} liked tracks for the first time. This may take a while. Subsequent operations will be instananeous"
        )
        # ? We can probably parallelize this
        for offset in range(20, limit, 20):
            self._liked_tracks.extend(
                [
                    LikedSong(**track)
                    for track in self.sp.current_user_saved_tracks(offset=offset).get(
                        "items"
                    )
                ]
            )
        return self._liked_tracks

    def get_tracks_month_year(self) -> pd.DataFrame:
        def agg_track_ids(x) -> list[str]:
            return x["track"].apply(lambda x: x.get("id")).to_list()

        df = pd.DataFrame([model.model_dump() for model in self.get_liked_tracks])
        df["added_at"] = pd.to_datetime(df["added_at"])
        gb = df.groupby(
            [
                df["added_at"].dt.year.rename("year"),
                df["added_at"].dt.month.rename("month"),
            ]
        )
        return (
            gb.apply(lambda x: agg_track_ids(x))
            .reset_index()
            .rename(columns={0: "track_ids"})
        )
