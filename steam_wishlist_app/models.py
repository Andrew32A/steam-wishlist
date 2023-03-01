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

class Game(db.Model):
    """Game model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(500), nullable=False)
    publish_date = db.Column(db.Date)

    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    publisher = db.relationship('Publisher', back_populates='games')

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
    games = db.relationship('Game', back_populates='publisher')

    def __str__(self):
        return f'<Publisher: {self.name}>'

    def __repr__(self):
        return f'<Publisher: {self.name}>'

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
