from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from steam_wishlist_app.models import Audience, Book, Author, Genre, User

class BookForm(FlaskForm):
    """Form to create a book."""
    title = StringField('Game Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    publish_date = DateField('Date Published')
    author = QuerySelectField('Publisher',
        query_factory=lambda: Author.query, allow_blank=False)
    audience = SelectField('Audience', choices=Audience.choices())
    genres = QuerySelectMultipleField('Genres',
        query_factory=lambda: Genre.query)
    submit = SubmitField('Submit')


class AuthorForm(FlaskForm):
    """Form to create an author."""
    name = StringField('Publisher Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    biography = TextAreaField('Publisher Description')
    submit = SubmitField('Submit')


class GenreForm(FlaskForm):
    """Form to create a genre."""
    name = StringField('Genre Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')