from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from steam_wishlist_app.models import Game, Publisher, User

class GameForm(FlaskForm):
    """Form to create a game."""
    title = StringField('Game Title',
        validators=[DataRequired(), Length(min=3, max=80)])
    image = StringField('Image',
        validators=[DataRequired(), Length(min=3, max=500)])
    publish_date = DateField('Date Published')
    publisher = QuerySelectField('Publisher',
        query_factory=lambda: Publisher.query, allow_blank=False)
    submit = SubmitField('Submit')


class AuthorForm(FlaskForm):
    """Form to create an publisher."""
    name = StringField('Publisher Name',
        validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')