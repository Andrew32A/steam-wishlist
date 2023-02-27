"""Create database models to represent tables."""
from steam_wishlist_app.extensions import db
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class Audience(FormEnum):
    CHILDREN = 'Children'
    YOUNG_ADULT = 'Young Adult'
    ADULT = 'Adult'
    ALL = 'All'

class Game(db.Model):
    """Game model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    publish_date = db.Column(db.Date)

    # The publisher - Who wrote it?
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    publisher = db.relationship('Publisher', back_populates='games')
    
    # The audience - Who is this game written for?
    audience = db.Column(db.Enum(Audience), default=Audience.ALL)

    # The genres, e.g. fiction, sci-fi, fantasy
    genres = db.relationship(
        'Genre', secondary='game_genre', back_populates='games')

    # Who favorited this game?
    users_who_favorited = db.relationship(
        'User', secondary='user_game', back_populates='favorite_games')

    def __str__(self):
        return f'<Game: {self.title}>'

    def __repr__(self):
        return f'<Game: {self.title}>'

class Publisher(db.Model):
    """Publisher model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.String(200))
    games = db.relationship('Game', back_populates='publisher')

    def __str__(self):
        return f'<Publisher: {self.name}>'

    def __repr__(self):
        return f'<Publisher: {self.name}>'

class Genre(db.Model):
    """Genre model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    games = db.relationship(
        'Game', secondary='game_genre', back_populates='genres')

    def __str__(self):
        return f'<Genre: {self.name}>'

    def __repr__(self):
        return f'<Genre: {self.name}>'

game_genre_table = db.Table('game_genre',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    favorite_games = db.relationship(
        'Game', secondary='user_game', back_populates='users_who_favorited')

    def __repr__(self):
        return f'<User: {self.username}>'

favorite_games_table = db.Table('user_game',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)
