from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from steam_wishlist_app.models import Game, Publisher, Genre, User

class GameForm(FlaskForm):
    """Form to create a game."""
    title = StringField('Game Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    publish_date = DateField('Date Published')
    publisher = QuerySelectField('Publisher',
        query_factory=lambda: Publisher.query, allow_blank=False)
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query)
    submit = SubmitField('Submit')


class AuthorForm(FlaskForm):
    """Form to create an publisher."""
    name = StringField('Publisher Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')

# CHANGE TO TAGS?
class GenreForm(FlaskForm):
    """Form to create a genre."""
    name = StringField('Genre Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')