from models import Session, User, Song, Playlist, PrivatePlaylist, PlaylistsSongs

session = Session()

user1 = User(Id=1, userName='urasuk', firstName='Yurii', lastName='Yanio', email='yray422@gmail.com',
            password='12kjk345', phone='0682608928', userStatus=False)
user2 = User(Id=2, userName='ostap', firstName='Ostap', lastName='Ivanov', email='ostap123@gmail.com',
            password='fef3434', phone='0681539818', userStatus=False)

song1 = Song(songId=1, name='Shallow', productionYear=2018, length=3.12)
song2 = Song(songId=2, name='Californication', productionYear=2007, length=4.59)

playlist1 = Playlist(playlistId=1, name='Urasuk_Party')
playlist2 = Playlist(playlistId=2, name='ClassicalMusic')

private_Playlist1 = PrivatePlaylist(privateplaylistId=1, playlistId=1, Id=1)


playlistsSongs1 = PlaylistsSongs(songId=1, playlistId=1)
playlistsSongs2 = PlaylistsSongs(songId=2, playlistId=1)
playlistsSongs3 = PlaylistsSongs(songId=1, playlistId=2)


session.add(user1)
session.add(user2)
session.add(user2)

session.add(song1)
session.add(song2)

session.add(playlist1)
session.add(playlist2)

session.commit()

session.add(private_Playlist1)

session.commit()

session.add(playlistsSongs1)
session.add(playlistsSongs2)
session.add(playlistsSongs3)

session.commit()

print(session.query(User).all()[0])
print(session.query(Song).all()[1])
print(session.query(Playlist).all())
print(session.query(PrivatePlaylist).all())
print(session.query(PlaylistsSongs).all())

session.close()