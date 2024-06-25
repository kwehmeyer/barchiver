"""Models"""
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Any
from .configuration import BARCHIVER_SETTINGS


class Artist(BaseModel):
    href: HttpUrl
    id: str
    name: str
    type: str
    uri: str


class Image(BaseModel):
    height: int
    url: HttpUrl
    width: int


class Album(BaseModel):
    album_type: str
    artists: List[Artist]
    href: HttpUrl
    id: str
    images: List[Image]
    name: str
    release_date: str
    release_date_precision: str
    total_tracks: int
    type: str
    uri: str


class Track(BaseModel):
    album: Album
    artists: List[Artist]
    disc_number: int
    duration_ms: int
    explicit: bool
    href: HttpUrl
    id: str
    is_local: bool
    name: str
    popularity: int
    preview_url: Optional[HttpUrl]
    track_number: int
    type: str
    uri: str


class LikedSong(BaseModel):
    added_at: str
    track: Track


class Owner(BaseModel):
    display_name: str
    external_urls: dict[str, HttpUrl]
    href: HttpUrl
    id: str
    type: str
    uri: str


class Playlist(BaseModel):
    collaborative: bool
    description: str = BARCHIVER_SETTINGS.playlist_signature
    external_urls: dict[str, HttpUrl]
    href: HttpUrl
    id: str
    images: Optional[Any]
    name: str
    owner: Owner
    primary_color: Optional[Any]
    public: bool
    snapshot_id: str
    tracks: Optional[dict]
    type: str
    uri: str
