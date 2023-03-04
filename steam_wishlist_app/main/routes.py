"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from steam_wishlist_app.models import Game, Publisher, User
from steam_wishlist_app.main.forms import GameForm, AuthorForm
from steam_wishlist_app.extensions import db, bcrypt

main = Blueprint("main", __name__)

def init_db():
    db.drop_all()
    db.create_all()

    a1 = Publisher(name='FromSoftware')
    a2 = Publisher(name='Team Cherry')
    a3 = Publisher(name="Kinetic Games")
    a4 = Publisher(name="Santa Monica Studio")
    a5 = Publisher(name="Poncie")
    a6 = Publisher(name="Coffee Stain Studios")
    a7 = Publisher(name="Motion Twin")
    a8 = Publisher(name="Valve")

    a99 = Publisher(name="Not on list")
    db.session.add(a99)

    b1 = Game(
        title='Bloodborne',
        publish_date=date(2015, 3, 24),
        publisher=a1,
        image="https://image.api.playstation.com/vulcan/img/rnd/202010/2614/NVmnBXze9ElHzU6SmykrJLIV.png",
    )
    db.session.add(b1)

    b2 = Game(
        title='Hollow Knight',
        publish_date=date(2017, 2, 24),
        publisher=a2,
        image="https://cdn.cloudflare.steamstatic.com/steam/apps/367520/capsule_616x353.jpg?t=1667006028"
    )
    db.session.add(b2)

    b3 = Game(
        title="Elden Ring",
        publish_date=date(2022, 2, 25),
        publisher=a1,
        image="https://image.api.playstation.com/vulcan/ap/rnd/202110/2000/phvVT0qZfcRms5qDAk0SI3CM.png"
    )
    db.session.add(b3)

    b4 = Game(
        title="Phasmophobia",
        publish_date=date(2020, 11, 18),
        publisher=a3,
        image="https://cdn.cloudflare.steamstatic.com/steam/apps/739630/capsule_616x353.jpg?t=1674232976"
    )
    db.session.add(b4)

    b5 = Game(
        title="God of War",
        publish_date=date(2005, 3, 22),
        publisher=a4,
        image="https://cdn.akamai.steamstatic.com/steam/apps/1593500/capsule_616x353.jpg?t=1642526157"
    )
    db.session.add(b5)

    b5 = Game(
        title="Vampire Survivors",
        publish_date=date(2021, 12, 17),
        publisher=a5,
        image="https://upload.wikimedia.org/wikipedia/en/e/e6/Vampire_Survivors_key_art.jpg"
    )
    db.session.add(b5)

    b6 = Game(
        title="Deep Rock Galactic",
        publish_date=date(2018, 2, 28),
        publisher=a6,
        image="https://image.api.playstation.com/vulcan/ap/rnd/202010/1407/2JSde8PFCF6B4nO2EECrcR1m.png"
    )
    db.session.add(b6)

    b7= Game(
        title="Dead Cells",
        publish_date=date(2018, 7, 7),
        publisher=a7,
        image="https://cdn.akamai.steamstatic.com/steam/apps/588650/capsule_616x353.jpg?t=1670838157"
    )
    db.session.add(b7)

    b8= Game(
        title="Left 4 Dead 2",
        publish_date=date(2009, 11, 17),
        publisher=a8,
        image="https://cdn.akamai.steamstatic.com/steam/apps/550/capsule_616x353.jpg?t=1675801903"
    )
    db.session.add(b8)

    u1 = User(
        username="test-user",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u1)

    u2 = User(
        username="Alex",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u2)

    u3 = User(
        username="Josh",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u3)

    u4 = User(
        username="Brian",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u4)

    u5 = User(
        username="Lon",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u5)

    u6 = User(
        username="Mark",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u6)

    u7 = User(
        username="Andrew",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u7)

    u8 = User(
        username="Isabella",
        password=bcrypt.generate_password_hash("1").decode('utf-8')
    )
    db.session.add(u8)

    db.session.commit()

init_db()

@main.route('/')
def homepage():
    all_games = Game.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_games=all_games, all_users=all_users)


@main.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()

    # if form was submitted and contained no errors
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
    
    # if form was not valid, or was not submitted yet
    return render_template('create_publisher.html', form=form)

@main.route('/game/<game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = GameForm(obj=game)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        game.title = form.title.data
        game.image = form.image.data
        game.publish_date = form.publish_date.data
        game.publisher = form.publisher.data

        db.session.commit()

        flash('Game was updated successfully.')
        return redirect(url_for('main.game_detail', game_id=game_id))

    return render_template('game_detail.html', game=game, form=form)


@main.route('/profile/<username>')
def profile(username):
    all_games = Game.query.all()
    user = User.query.filter_by(username=username).one()

    user_wishlist = user.favorite_games

    return render_template('profile.html', user=user, all_games=all_games, user_wishlist=user_wishlist)


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
