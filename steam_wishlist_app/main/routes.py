"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from steam_wishlist_app.models import Game, Publisher, Genre, User
from steam_wishlist_app.main.forms import BookForm, AuthorForm, GenreForm

# Import app and db from events_app package so that we can run app
from steam_wishlist_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

def create_games():
    a1 = Publisher(name='FromSoftware')
    b1 = Game(
        title='Bloodborne',
        publish_date=date(2015, 3, 24),
        publisher=a1
    )
    db.session.add(b1)

    a2 = Publisher(name='Team Cherry')
    b2 = Game(
        title='Hollow Knight',
        publish_date=date(2017, 2, 24),
        publisher=a2)
    db.session.add(b2)
    db.session.commit()
# create_games()


@main.route('/')
def homepage():
    all_games = Game.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_games=all_games, all_users=all_users)


@main.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_game = Game(
            title=form.title.data,
            publish_date=form.publish_date.data,
            publisher=form.publisher.data,
            audience=form.audience.data,
            genres=form.genres.data
        )
        db.session.add(new_game)
        db.session.commit()

        flash('New game was added successfully.')
        return redirect(url_for('main.game_detail', game_id=new_game.id))
    return render_template('create_game.html', form=form)


@main.route('/create_author', methods=['GET', 'POST'])
@login_required
def create_author():
    form = AuthorForm()
    if form.validate_on_submit():
        new_publisher = Publisher(
            name=form.name.data,
            biography=form.biography.data
        )
        db.session.add(new_publisher)
        db.session.commit()

        flash('New publisher was added successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_author.html', form=form)


@main.route('/create_genre', methods=['GET', 'POST'])
@login_required
def create_genre():
    form = GenreForm()
    if form.validate_on_submit():
        new_genre = Genre(
            name=form.name.data
        )
        db.session.add(new_genre)
        db.session.commit()

        flash('New genre created successfully.')
        return redirect(url_for('main.homepage'))
    
    # if form was not valid, or was not submitted yet
    return render_template('create_genre.html', form=form)


@main.route('/game/<game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = BookForm(obj=game)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        game.title = form.title.data
        game.publish_date = form.publish_date.data
        game.publisher = form.publisher.data
        game.audience = form.audience.data
        game.genres = form.genres.data

        db.session.commit()

        flash('Game was updated successfully.')
        return redirect(url_for('main.game_detail', game_id=game_id))

    return render_template('game_detail.html', game=game, form=form)


@main.route('/profile/<username>')
def profile(username):
    all_games = Game.query.all()

    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user, all_games=all_games)


@main.route('/favorite/<game_id>', methods=['POST'])
@login_required
def favorite_game(game_id):
    game = Game.query.get(game_id)
    if game in current_user.favorite_games:
        flash('Game already in wishlist.')
    else:
        current_user.favorite_games.append(game)
        db.session.add(current_user)
        db.session.commit()
        flash('Game added to wishlist.')
    return redirect(url_for('main.game_detail', game_id=game_id))


@main.route('/unfavorite/<game_id>', methods=['POST'])
@login_required
def unfavorite_game(game_id):
    game = Game.query.get(game_id)
    if game not in current_user.favorite_games:
        flash('Game not in wishlist.')
    else:
        current_user.favorite_games.remove(game)
        db.session.add(current_user)
        db.session.commit()
        flash('Game removed from wishlist.')
    return redirect(url_for('main.game_detail', game_id=game_id))
