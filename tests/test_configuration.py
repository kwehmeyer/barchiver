from barchiver.configuration import BArchiverConfig
import os


def test_barchiver_config():
    os.environ["SPOTIFY_CLIENT_ID"] = "your_client_id"
    os.environ["SPOTIFY_CLIENT_SECRET"] = "your_client_secret"
    config = BArchiverConfig()
    # Test setting values
    assert config.spotify_client_id == "your_client_id"
    assert config.spotify_client_secret == "your_client_secret"
