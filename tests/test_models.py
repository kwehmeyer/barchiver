from barchiver.models import Track, Album, Artist, Image


def test_track_model() -> None:
    """Test the Track model"""

    # Create sample data
    album = Album(
        album_type="album",
        artists=[
            Artist(
                href="https://example.com/artist",
                id="artist_id",
                name="Artist",
                type="artist",
                uri="spotify:artist:artist_id",
            )
        ],
        href="https://example.com/album",
        id="album_id",
        images=[Image(height=640, url="https://example.com/image.jpg", width=640)],
        name="Album",
        release_date="2022-01-01",
        release_date_precision="day",
        total_tracks=10,
        type="album",
        uri="spotify:album:album_id",
    )
    artists = [
        Artist(
            href="https://example.com/artist",
            id="artist_id",
            name="Artist",
            type="artist",
            uri="spotify:artist:artist_id",
        )
    ]
    track = Track(
        album=album,
        artists=artists,
        disc_number=1,
        duration_ms=180000,
        explicit=False,
        href="https://example.com/track",
        id="track_id",
        is_local=False,
        name="Track",
        popularity=80,
        preview_url="https://example.com/preview.mp3",
        track_number=5,
        type="track",
        uri="spotify:track:track_id",
    )

    # Test the model fields
    assert track.album == album
    assert track.artists == artists
    assert track.disc_number == 1
    assert track.duration_ms == 180000
    assert not track.explicit
    assert track.id == "track_id"
    assert not track.is_local
    assert track.name == "Track"
    assert track.popularity == 80
    assert track.track_number == 5
    assert track.type == "track"
    assert track.uri == "spotify:track:track_id"
