from barchiver.configuration import BArchiverConfig


def test_barchiver_config():
    config = BArchiverConfig()

    # Test default values
    assert config.spotify_client_id == ""
    assert config.spotify_client_secret == ""

    # Test setting values
    config.spotify_client_id = "your_client_id"
    config.spotify_client_secret = "your_client_secret"
    assert config.spotify_client_id == "your_client_id"
    assert config.spotify_client_secret == "your_client_secret"
