from barchiver.repository import UserRepository
from barchiver.models import LikedSong
from conftest import sp


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
