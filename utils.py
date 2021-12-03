from models import Session, User, Song, Playlist, PrivatePlaylist, PlaylistsSongs


def find_by_id(model, id):
    session = Session()
    try:
        t = session.query(model).filter_by(id=id).one()
    except:
        return None
    return t


def find_by_email(email):
    session = Session()
    try:
        user = session.query(User).filter_by(email=email).one()
    except:
        return None
    return user


def find_by_username(userName):
    session = Session()
    try:
        user = session.query(User).filter_by(userName=userName).one()
    except:
        return None
    return user


def update_util(model, data):
    try:
        if data.get('userName', None):
            model.userName = data['userName']
        if data.get('password', None):
            model.password = data['password']
        if data.get('firstName', None):
            model.firstName = data['firstName']
        if data.get('lastName', None):
            model.lastName = data['lastName']
        if data.get('email', None):
            model.email = data['email']
        if data.get('phone', None):
            model.phone = data['phone']
        if data.get('name', None):
            model.name = data['name']
        if data.get('productionYear', None):
            model.productionYear = data['productionYear']
        if data.get('length', None):
            model.length = data['length']
        if data.get('Id', None):
            model.Id = data['Id']
        if data.get('songId', None):
            model.songId = data['songId']
        if data.get('playlistId', None):
            model.playlistId = data['playlistId']

    except:
        return None

    return model
