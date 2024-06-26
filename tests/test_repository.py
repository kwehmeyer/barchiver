from barchiver.repository import UserRepository
from pandas import DataFrame
from barchiver.models import LikedSong
from conftest import sp
import pandas as pd
from barchiver.models import Playlist


class TestUserRepository:
    def test_create_user_repo(self):
        """Test if UserRepository can be created"""
        user_repo = UserRepository(sp)
        assert hasattr(user_repo, "sp")
        self.repo = user_repo

    def test_get_liked_tracks(self):
        """Test if UserRepository can get liked tracks"""
        user_repo = UserRepository(sp)
        liked = user_repo.get_liked_tracks
        assert isinstance(liked, list)
        assert len(liked) > 0
        assert isinstance(liked[0], LikedSong)

    def test_get_tracks_month_year(self):
        """Test if UserRepository can get tracks grouped by month and year"""
        user_repo = UserRepository(sp)
        tracks_month_year = user_repo.get_tracks_month_year()
        assert isinstance(tracks_month_year, DataFrame)
        assert "year" in tracks_month_year.columns
        assert "month" in tracks_month_year.columns
        assert "track_ids" in tracks_month_year.columns

    def test_get_barchiver_playlists(self):
        """Test if UserRepository can get Barchiver playlists"""
        user_repo = UserRepository(sp)
        sp.user_playlist_create(
            user=sp.me().get("id"),
            name="test",
            public=True,
            description="barchiver_test",
        )
        playlists = user_repo.get_barchiver_playlists(filter_term="barchiver_test")
        assert isinstance(playlists, list)
        assert len(playlists) > 0
        assert isinstance(playlists[0], Playlist)
        user_repo.delete_barchiver_playlists(filter_term="barchiver_test")

    def test_delete_barchiver_playlists(self):
        user_repo = UserRepository(sp)
        sp.user_playlist_create(
            user=sp.me().get("id"),
            name="test",
            public=True,
            description="barchiver_test",
        )
        user_repo.delete_barchiver_playlists(filter_term="barchiver_test")
        playlists = user_repo.get_barchiver_playlists(filter_term="barchiver_test")
        assert len(playlists) == 0

    def test_create_archival_playlists(self, mocker):
        """Test if UserRepository can create archival playlists"""
        user_repo = UserRepository(sp)
        mocker.patch.object(
            user_repo,
            "get_tracks_month_year",
            return_value=pd.DataFrame(
                {
                    "year": [2022, 2022],
                    "month": [1, 2],
                    "track_ids": [
                        ["track_id_1", "track_id_2"],
                        ["track_id_3", "track_id_4"],
                    ],
                }
            ),
        )
        mocker.patch.object(user_repo.sp, "user_playlist_create")
        mocker.patch.object(user_repo.sp, "playlist_add_items")

        user_repo.create_archival_playlists()

        assert user_repo.get_tracks_month_year.call_count == 1
        assert user_repo.sp.user_playlist_create.call_count == 2
        assert user_repo.sp.playlist_add_items.call_count == 2
