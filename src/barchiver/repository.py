"""Respositories for the Barchiver application."""
from spotipy import Spotify
from .models import LikedSong, Playlist
from loguru import logger
import pandas as pd
import calendar
from .configuration import BARCHIVER_SETTINGS


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

    def get_barchiver_playlists(
        self, filter_term=BARCHIVER_SETTINGS.playlist_signature
    ):
        initial_call = self.sp.current_user_playlists()
        if initial_call.get("total") <= 50:
            return list(
                filter(
                    lambda x: filter_term in x["description"], initial_call.get("items")
                )
            )
        results = []
        for idx in range(0, initial_call.get("total"), 50):
            results.extend(
                list(
                    filter(
                        lambda x: filter_term in x["description"],
                        self.sp.current_user_playlists(offset=idx).get("items"),
                    )
                )
            )
        return [Playlist(**playlist) for playlist in results]

    def delete_barchiver_playlists(
        self, filter_term=BARCHIVER_SETTINGS.playlist_signature
    ) -> None:
        playlists = self.get_barchiver_playlists(filter_term=filter_term)
        for playlist in playlists:
            self.sp.current_user_unfollow_playlist(playlist.id)

    def create_archival_playlists(self):
        for idx, row in self.get_tracks_month_year().iterrows():
            month = calendar.month_name[int(row["month"])]
            playlist_name = f"{month} {row["year"]}"
            ids = row[
                "track_ids"
            ]  # Is this stupid? Yes, does it break without it? Yes. Do I know why? no.
            playlist = self.sp.user_playlist_create(
                user=id,
                name=playlist_name,
                public=False,
                description=BARCHIVER_SETTINGS.playlist_signature,
            )
            # TODO: can we speed this up? maybe a map or apply?
            # fuckit we ball - sort it out later
            for i in range(0, len(ids), 100):
                self.sp.playlist_add_items(
                    playlist_id=playlist["id"], items=ids[i : i + 100]
                )
