from sqlalchemy import create_engine, Integer, Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Соединение с базой данных
engine = create_engine('sqlite:///server.db', echo=False)
Base = declarative_base()


# Определение таблицы в базе данных
class Sql_users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    language = Column(String)
    telegram_language = Column(String)
    subscription = Column(Boolean, default=True)
    permissions = Column(String, default='')
    last_timer_time = Column(DateTime)
    registration_date = Column(DateTime)

    anime_playlist = relationship('Sql_anime_playlist', lazy='joined')


    def __init__(self, telegram_id, username, first_name, last_name, language):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.registration_date = datetime.now()
        self.telegram_language = language
        self.language = language


class Sql_anime_playlist(Base):
    __tablename__ = "anime_playlist"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id: int = Column(Integer, ForeignKey('anime.id'))
    series = Column(Integer, nullable=False, default=1)
    state = Column(String, nullable=False, default='watching')


class Sql_anime(Base):
    __tablename__ = 'anime'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    names = Column(String)
    season = Column(Integer, nullable=False)
    series = Column(Integer, nullable=False)
    more_series = Column(Boolean, nullable=False)
    last_series = Column(Integer, nullable=False)
    last_update = Column(DateTime, default=datetime.now())
    year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    country = Column(String, nullable=False)
    description = Column(String, nullable=False)
    anime_type = Column(String, nullable=False)
    image = Column(String, nullable=False)
    t_image_id = Column(String)

    anime_urls = relationship('Sql_anime_urls', lazy='joined')
    anime_playlist = relationship('Sql_anime_playlist', lazy='joined')


    def __init__(self,
                 name: str,
                 season: int,
                 series: int,
                 last_series: int,
                 year: int,
                 genre: str,
                 country: str,
                 description: str,
                 anime_type: str,
                 image: str,
                 more_series: bool
                 ):
        self.name = name
        self.season = season
        self.series = series
        self.last_series = last_series
        self.year = year
        self.genre = genre
        self.country = country
        self.description = description
        self.anime_type = anime_type
        self.image = image
        self.more_series = more_series


class Sql_anime_urls(Base):
    __tablename__ = 'anime_urls'

    id = Column(Integer, primary_key=True)
    anime_id = Column(String, ForeignKey('anime.id'))
    url_type = Column(String, nullable=False)
    site = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)


    def __init__(self, anime_id, url):
        self.anime_id = anime_id
        self.url = url
        self.url_type = 'site'
        if 'anime-bit' in url:
            self.site = 'anime-bit'


class Sql_users_log(Base):
    __tablename__ = 'user_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    text = Column(String)
    datetime = Column(DateTime)


    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text
        self.datetime = datetime.now()


# Создание таблицы
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
