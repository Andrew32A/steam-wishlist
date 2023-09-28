"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from steam_wishlist_app.models import Game, Publisher, User
from steam_wishlist_app.main.forms import GameForm, AuthorForm
from steam_wishlist_app.extensions import db, bcrypt

main = Blueprint("main", __name__)

# helper function to seed database

# landing page that displays all games and users
@main.route('/')
def homepage():
    all_games = Game.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_games=all_games, all_users=all_users)

# create games
@main.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()

    if form.validate_on_submit(): 
        new_game = Game(
            title=form.title.data,
            image=form.image.data,
            publish_date=form.publish_date.data,
            publisher=form.publisher.data,
        )
        db.session.add(new_game)
        db.session.commit()

        flash('New game was added successfully.')
        return redirect(url_for('main.game_detail', game_id=new_game.id))
    return render_template('create_game.html', form=form)

# create publishers
@main.route('/create_publisher', methods=['GET', 'POST'])
@login_required
def create_author():
    form = AuthorForm()

    if form.validate_on_submit():
        new_publisher = Publisher(
            name=form.name.data
        )
        db.session.add(new_publisher)
        db.session.commit()

        flash('New publisher was added successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_publisher.html', form=form)

@main.route('/game/<game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = GameForm(obj=game)
    
    if form.validate_on_submit():
        game.title = form.title.data
        game.image = form.image.data
        game.publish_date = form.publish_date.data
        game.publisher = form.publisher.data

        db.session.commit()

        flash('Game was updated successfully.')
        return redirect(url_for('main.game_detail', game_id=game_id))

    return render_template('game_detail.html', game=game, form=form)

# view user details
@main.route('/profile/<username>')
def profile(username):
    all_games = Game.query.all()
    user = User.query.filter_by(username=username).one()

    user_wishlist = user.favorite_games

    return render_template('profile.html', user=user, all_games=all_games, user_wishlist=user_wishlist)

# wishlist game
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

# unwishlist game
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

# delete game
@main.route('/delete_game/<game_id>', methods=['POST', 'GET'])
@login_required
def delete_game(game_id):
    game = Game.query.filter_by(id=game_id).one()

    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('main.homepage'))