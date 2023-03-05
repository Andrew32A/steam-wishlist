import unittest
import app

from datetime import date
from steam_wishlist_app.extensions import app, db, bcrypt
from steam_wishlist_app.models import Game, Publisher, User
from flask_login import login_user, logout_user, login_required, current_user

"""
run tests with:
python -m unittest steam_wishlist_app.main.tests
"""

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_games():
    a1 = Publisher(name='Team Cherry')
    g1 = Game(
        title='Hallow Knight',
        publish_date=date(1960, 7, 11),
        publisher=a1
    )
    db.session.add(g1)
    db.session.commit()

def create_user():
    # creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        create_games()
        create_user()

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Hallow Knight', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        self.assertNotIn('Create Game', response_text)
        self.assertNotIn('Create Publisher', response_text)
        self.assertNotIn('Create Genre', response_text)
 
    def test_homepage_logged_in(self):
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Hallow Knight', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Create Game', response_text)
        self.assertIn('Create Publisher', response_text)
        self.assertIn('Create Genre', response_text)

        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_create_game(self):
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        post_data = {
            'title': 'Bloodborne',
            'publish_date': '2015-07-14',
            'publisher': 1,
            'genres': []
        }
        self.app.post('/create_game', data=post_data)

        created_game = Game.query.filter_by(title='Bloodborne').one()
        self.assertIsNotNone(created_game)
        self.assertEqual(created_game.publisher.name, 'FromSoftware')

    def test_create_game_logged_out(self):
        create_games()
        create_user()

        response = self.app.get('/create_game')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_game', response.location)

    def test_favorite_game(self):
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/profile/me1', follow_redirects=True)
        post_data = response.get_data(as_text=True)
        self.app.post('/favorite/1', data=post_data)

        second_response = self.app.get('/profile/me1', follow_redirects=True)
        second_response_data = second_response.get_data(as_text=True)
        self.assertIn("Hallow Knight", second_response_data)

    def test_unfavorite_game(self):
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('profile.me1', follow_redirects=True)
        post_data = response.get_data(as_text=True)
        self.app.post('/unfavorite/1', data=post_data)

        second_response = self.app.get('/profile/me1', follow_redirects=True)
        second_response_data = second_response.get_data(as_text=True)
        self.assertNotIn("Hallow Knight", second_response_data)
        