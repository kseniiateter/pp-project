from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Boolean,
    DECIMAL,
    PrimaryKeyConstraint,
)
from sqlalchemy import orm, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:mySQL.kt.1502@localhost:3306/pp_music"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    Id = Column(Integer, primary_key=True)
    userName = Column(String(20), nullable=False)
    firstName = Column(String(20), nullable=False)
    lastName = Column(String(25), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    phone = Column(String(10))
    userStatus = Column(Boolean)

    def __repr__(self):
        return "<User('%s','%s','%s','%s','%s','%s','%s','%s',)>" % (self.Id, self.userStatus, self.userName,
                                                                     self.firstName, self.lastName, self.email,
                                                                     self.password, self.phone)

    def __str__(self):
        return f"Id: {self.Id}\n" \
               f"userStatus: {self.userStatus}\n" \
               f"userName: {self.userName}\n" \
               f"firstName: {self.firstName}\n" \
               f"lastName: {self.lastName}\n" \
               f"email: {self.email}\n" \
               f"password: {self.password}\n" \
               f"phone: {self.phone}\n"


class Song(Base):
    __tablename__ = "song"

    songId = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    productionYear = Column(Integer)
    length = Column(DECIMAL(10, 2))

    def __repr__(self):
        return "<Song('%s','%s','%s','%s')>" % (self.songId, self.name, self.productionYear, self.length)

    def __str__(self):
        return f"songId: {self.songId}\n" \
               f"name: {self.name}\n" \
               f"productionYear: {self.productionYear}\n" \
               f"length: {self.length}\n"


class Playlist(Base):
    __tablename__ = "playlist"

    playlistId = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return "<Song('%s','%s')>" % (self.playlistId, self.name)

    def __str__(self):
        return f"playlistid: {self.playlistId}\n" \
               f"name: {self.name}\n"


class PlaylistsSongs(Base):
    __tablename__ = "playlistssongs"

    songId = Column(Integer, ForeignKey('song.songId'))
    playlistId = Column(Integer, ForeignKey('playlist.playlistId'))

    song = orm.relationship("Song")
    playlist = orm.relationship("Playlist")

    __table_args__ = (
        PrimaryKeyConstraint('songId', 'playlistId'), {}
    )


class PrivatePlaylist(Base):
    __tablename__ = "privateplaylist"

    privateplaylistId = Column(Integer, primary_key=True)
    playlistId = Column(Integer, ForeignKey('playlist.playlistId'))
    Id = Column(Integer, ForeignKey('user.Id'))

    user = orm.relationship("User")
    playlist = orm.relationship("Playlist")

    def __repr__(self):
        return "<Privateplaylist('%s')>" % self.privateplaylistId

    def __str__(self):
        return f"privateplaylistId: {self.privateplaylistId}\n"
