from flask import Flask, request, jsonify
from constants import *
from schemas import *
from utils import *
import bcrypt
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route("/api/v1/hello-world-9")
def hello_world():
    return "<p>Hello World 9</p>"


@auth.verify_password
def user_auth(username, password):
    session = Session()
    try:
        user = session.query(User).filter_by(userName=username).one()
    except:
        return jsonify(BAD_USERNAME), 404
    if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        return username, 200
    else:
        return jsonify(BAD_PASSWORD), 401


# All about user
@app.route(BASE_PATH + USER_PATH, methods=['POST'])
def create_user():
    session = Session()
    try:
        user_request = request.get_json()
        email = user_request['email']
        username = user_request['userName']

        if find_by_email(email) is not None or find_by_username(username) is not None:
            return jsonify(USER_ALREADY_EXISTS), 400

        # password hashing ------------------------------------
        passwd = user_request.get('password')
        b = bytes(passwd, 'utf-8')
        hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
        user_request['password'] = hashed_password
        # -----------------------------------------------------

        user = User(**user_request)

        session.add(user)
        session.commit()

        return jsonify(USER_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['GET'])
@auth.login_required
def get_user_by_id(Id):
    session = Session()
    auth_rez = auth.current_user()

    user1 = session.query(User).filter_by(userName=auth_rez[0]).one()

    if int(Id) != user1.Id:
        return jsonify(ACCESS_DENIED), 403

    try:
        user = session.query(User).filter_by(Id=int(Id)).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    user1 = session.query(User).filter_by(userName=auth_rez[0]).one()

    if int(Id) != user1.Id:
        return jsonify(ACCESS_DENIED), 403

    return jsonify(UserSchema().dump(user)), 200


@app.route(BASE_PATH + USER_PATH, methods=['GET'])
def get_all_users():
    session = Session()
    try:
        users = session.query(User).all()
    except:
        users = []

    users_dto = UserSchema(many=True)

    return jsonify(users_dto.dump(users)), 200


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['PUT'])
@auth.login_required
def update_user(Id):
    session = Session()
    auth_rez = auth.current_user()

    try:
        session.query(User).filter_by(Id=int(Id)).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    user1 = session.query(User).filter_by(userName=auth_rez[0]).one()

    if int(Id) != user1.Id:
        return jsonify(ACCESS_DENIED), 403

    try:
        if request.json['Id']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()

        user = session.query(User).filter_by(Id=Id).one()

        if update_request.get('password'):
            # password hashing ------------------------------------
            passwd = update_request.get('password')
            b = bytes(passwd, 'utf-8')
            hashed_password = bcrypt.hashpw(b, bcrypt.gensalt())
            update_request['password'] = hashed_password
            # -----------------------------------------------------

        updated_user = update_util(user, update_request)

        if updated_user is None:
            return jsonify(SOMETHING_WENT_WRONG), 400
        session.commit()
        return jsonify(USER_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + USER_PATH + '/' + '<int:Id>', methods=['DELETE'])
@auth.login_required
def delete_user(Id):
    session = Session()
    auth_rez = auth.current_user()

    user1 = session.query(User).filter_by(userName=auth_rez[0]).one()

    if int(Id) != user1.Id:
        return jsonify(ACCESS_DENIED), 403

    try:
        session.query(User).filter_by(Id=int(Id)).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    user = session.query(User).filter_by(Id=Id).one()

    session.delete(user)
    session.commit()

    return jsonify(USER_DELETED), 200


# All about song
@app.route(BASE_PATH + SONG_PATH, methods=['POST'])
@auth.login_required
def place_song():
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    try:
        song_request = request.get_json()

        song = Song(**song_request)

        session.add(song)
        session.commit()

        return jsonify(SONG_PLACED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + SONG_PATH + '/' + '<int:songId>', methods=['GET'])
@auth.login_required
def get_song_by_id(songId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        song = session.query(Song).filter_by(songId=songId).one()
    except:
        return jsonify(SONG_NOT_FOUND), 404

    return jsonify(SongSchema().dump(song)), 200


@app.route(BASE_PATH + SONG_PATH, methods=['GET'])
@auth.login_required
def get_all_songs():
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        songs = session.query(Song).all()
    except:
        songs = []

    song_dto = SongSchema(many=True)

    return jsonify(song_dto.dump(songs)), 200


@app.route(BASE_PATH + SONG_PATH + '/' + '<int:songId>', methods=['DELETE'])
@auth.login_required
def delete_song(songId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        song = session.query(Song).filter_by(songId=songId).one()
    except:
        return jsonify(SONG_NOT_FOUND), 404
    session.delete(song)
    session.commit()

    return jsonify(SONG_DELETED), 200


@app.route(BASE_PATH + SONG_PATH + '/' + '<int:songId>', methods=['PUT'])
@auth.login_required
def edit_song(songId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        if request.json['songId']:
            return jsonify(CANT_CHANGE_ID), 400
    except:
        pass
    try:
        update_request = request.get_json()

        try:
            song = session.query(Song).filter_by(songId=songId).one()
        except:
            return jsonify(SONG_NOT_FOUND), 404

        update_song = update_util(song, update_request)

        if update_song is None:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.commit()
        return jsonify(SONG_EDITED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400

    # update_request = request.get_json()
    #
    # try:
    #     song = session.query(Song).filter_by(songId=songId).one()
    # except:
    #     return jsonify(SONG_NOT_FOUND), 404
    #
    # update_song = update_util(song, update_request)
    #
    # if update_song == None:
    #     return jsonify(SOMETHING_WENT_WRONG), 400
    #
    # session.commit()
    # return jsonify(SONG_EDITED), 200


# All about playlist
@app.route(BASE_PATH + PLAYLIST_PATH, methods=['POST'])
@auth.login_required
def create_playlist():
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        playlist_request = request.get_json()

        playlist = Playlist(**playlist_request)

        session.add(playlist)
        session.commit()

        return jsonify(PLAYLIST_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + PLAYLIST_PATH + '/' + '<int:playlistId>', methods=['GET'])
@auth.login_required
def get_playlist_by_id(playlistId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    if session.query(PrivatePlaylist).filter_by(playlistId=playlistId).all():
        p_playlist = session.query(PrivatePlaylist).filter_by(playlistId=playlistId).one()
        user = session.query(User).filter_by(Id=p_playlist.Id).one()
        if user.userName != auth_rez[0]:
            return jsonify(PRIVATE_PLAYLIST), 404

    try:
        playlist = session.query(Playlist).filter_by(playlistId=playlistId).one()
    except:
        return jsonify(PLAYLIST_NOT_FOUND), 404

    return jsonify(PlaylistSchema().dump(playlist)), 200


# @app.route(BASE_PATH + PLAYLIST_PATH, methods=['GET'])
# @auth.login_required
# def get_all_playlists():
#     session = Session()
#     auth_rez = auth.current_user()
#     if auth_rez[1] != 200:
#         return auth_rez
#     try:
#         playlists = session.query(Playlist).all()
#     except:
#         playlists = []
#
#     playlist_dto = PlaylistSchema(many=True)
#
#     return jsonify(playlist_dto.dump(playlists)), 200


@app.route(BASE_PATH + PLAYLIST_PATH + '/public', methods=['GET'])
@auth.login_required
def get_all_public_playlists():
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    try:
        playlists = session.query(Playlist).all()
    except:
        playlists = []

    playlist_dto = PlaylistSchema(many=True)

    rez = playlist_dto.dump(playlists)
    print('start', rez)
    to_del = []
    for i in range(len(rez)):
        _playlistId = rez[i]['playlistId']
        if session.query(PrivatePlaylist).filter_by(playlistId=_playlistId).all():
            to_del.append(i)
    rez2 = []
    for i in range(len(rez)):
        if i not in to_del:
            rez2.append(rez[i])

    print('rez2', rez2)

    return jsonify(rez2), 200


@app.route(BASE_PATH + PLAYLIST_PATH + '/' + '<int:playlistId>', methods=['DELETE'])
@auth.login_required
def delete_playlist(playlistId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    if session.query(PrivatePlaylist).filter_by(playlistId=playlistId).all():
        p_playlist = session.query(PrivatePlaylist).filter_by(playlistId=playlistId).one()
        user = session.query(User).filter_by(Id=p_playlist.Id).one()
        if user.userName != auth_rez[0]:
            return jsonify(ACCESS_DENIED), 404
    try:
        playlist = session.query(Playlist).filter_by(playlistId=playlistId).one()
    except:
        return jsonify(PLAYLIST_NOT_FOUND), 404
    session.delete(playlist)
    session.commit()

    return jsonify(PLAYLIST_DELETED), 200


@app.route(BASE_PATH + PLAYLIST_PATH + '/' + '<int:playlistId>', methods=['PUT'])
@auth.login_required
def edit_playlist(playlistId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    if session.query(PrivatePlaylist).filter_by(playlistId=playlistId).all():
        p_playlist = session.query(PrivatePlaylist).filter_by(playlistId=playlistId).one()
        user = session.query(User).filter_by(Id=p_playlist.Id).one()
        if user.userName != auth_rez[0]:
            return jsonify(ACCESS_DENIED), 404

    try:
        if request.json['playlistId']:
            return jsonify(CANT_CHANGE_ID), 400

    except:
        pass
    try:
        update_request = request.get_json()

        try:
            playlist = session.query(Playlist).filter_by(playlistId=playlistId).one()
        except:
            return jsonify(PLAYLIST_NOT_FOUND), 404

        update_playlist = update_util(playlist, update_request)

        if update_playlist is None:
            return jsonify(SOMETHING_WENT_WRONG), 400

        session.commit()
        return jsonify(PLAYLIST_UPDATED), 200
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + PLAYLIST_PATH + '/' + '<int:playlistId>' + '/' + '<int:songId>', methods=['POST'])
@auth.login_required
def add_song(playlistId, songId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    if session.query(PrivatePlaylist).filter_by(playlistId=playlistId).all():
        p_playlist = session.query(PrivatePlaylist).filter_by(playlistId=playlistId).one()
        user = session.query(User).filter_by(Id=p_playlist.Id).one()
        if user.userName != auth_rez[0]:
            return jsonify(ACCESS_DENIED), 404

    try:
        session.query(Song).filter_by(songId=songId).one()
    except:
        return jsonify(SONG_NOT_FOUND), 404
    try:
        session.query(Playlist).filter_by(playlistId=playlistId).one()
    except:
        return jsonify(PLAYLIST_NOT_FOUND), 404

    if session.query(PlaylistsSongs).filter_by(playlistId=playlistId, songId=songId).all():
        return jsonify(SONG_ALREADY_IN_PLAYLIST), 400

    playlist_song = PlaylistsSongs(songId=songId, playlistId=playlistId)

    session.add(playlist_song)
    session.commit()

    return jsonify(SONG_ADDED_TO_PLAYLIST), 201


@app.route(BASE_PATH + PLAYLIST_PATH + '/' + '<int:playlistId>' + '/' + '<int:songId>', methods=['DELETE'])
@auth.login_required
def del_song(playlistId, songId):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    if session.query(PrivatePlaylist).filter_by(playlistId=playlistId).all():
        p_playlist = session.query(PrivatePlaylist).filter_by(playlistId=playlistId).one()
        user = session.query(User).filter_by(Id=p_playlist.Id).one()
        if user.userName != auth_rez[0]:
            return jsonify(ACCESS_DENIED), 404

    try:
        session.query(Song).filter_by(songId=songId).one()
    except:
        return jsonify(SONG_NOT_FOUND), 404
    try:
        session.query(Playlist).filter_by(playlistId=playlistId).one()
    except:
        return jsonify(PLAYLIST_NOT_FOUND), 404
    playlist_song = session.query(PlaylistsSongs).filter_by(playlistId=playlistId, songId=songId).one()

    session.delete(playlist_song)
    session.commit()

    return jsonify(SONG_DELETED_FROM_PLAYLIST), 201


# All about private playlist
@app.route(BASE_PATH + PRIVATE_PLAYLIST_PATH, methods=['POST'])
@auth.login_required
def create_private_playlist():
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez
    _playlistId = request.json['playlistId']
    if session.query(PrivatePlaylist).filter_by(playlistId=_playlistId).all():
        return jsonify(PLAYLIST_ALREADY_PRIVATE), 400

    try:

        private_playlist_request = request.get_json()

        user = session.query(User).filter_by(userName=auth_rez[0]).one()
        if private_playlist_request['Id'] != user.Id:
            return jsonify(ACCESS_DENIED)
        try:
            session.query(User).filter_by(Id=private_playlist_request['Id']).one()
        except:
            return jsonify(USER_NOT_FOUND), 404
        try:
            session.query(Playlist).filter_by(playlistId=private_playlist_request['playlistId']).one()
        except:
            return jsonify(PLAYLIST_NOT_FOUND), 404

        private_playlist = PrivatePlaylist(**private_playlist_request)

        session.add(private_playlist)
        session.commit()

        return jsonify(PRIVATE_PLAYLIST_CREATED), 201
    except:
        return jsonify(SOMETHING_WENT_WRONG), 400


@app.route(BASE_PATH + PRIVATE_PLAYLIST_PATH + '/' + '<int:Id>', methods=['GET'])
@auth.login_required
def get_private_playlists_by_id(Id):
    session = Session()
    auth_rez = auth.current_user()
    if auth_rez[1] != 200:
        return auth_rez

    user1 = session.query(User).filter_by(userName=auth_rez[0]).one()

    if int(Id) != user1.Id:
        return jsonify(ACCESS_DENIED), 403

    try:
        session.query(User).filter_by(Id=Id).one()
    except:
        return jsonify(USER_NOT_FOUND), 404

    try:
        private_playlists = session.query(PrivatePlaylist).filter_by(Id=Id).all()
    except:
        private_playlists = []

    private_playlists_dto = PrivatePlaylistSchema(many=True)

    return jsonify(private_playlists_dto.dump(private_playlists)), 200


if __name__ == '__main__':
    app.run()
