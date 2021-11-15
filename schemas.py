from models import User, Song, Playlist, PrivatePlaylist, PlaylistsSongs
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(Schema):
    class Meta:
        model = User
        fields = ('Id', 'userName', 'firstName', 'lastName', 'email', 'password', 'phone', 'userStatus')


class SongSchema(Schema):
    class Meta:
        model = Song
        fields = ('songId', 'name', 'productionYear')


class PlaylistSchema(Schema):
    class Meta:
        model = Playlist
        fields = ('playlistId', 'name')


class PrivatePlaylistSchema(Schema):
    class Meta:
        model = PrivatePlaylist
        fields = ('privateplaylistId', 'playlistId', 'Id')


class PlaylistsSongsSchema(Schema):
    class Meta:
        model = PlaylistsSongs
        fields = ('songId', 'playlistId')
