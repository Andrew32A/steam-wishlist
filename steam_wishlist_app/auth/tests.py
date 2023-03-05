import os
from unittest import TestCase

from datetime import date
 
from steam_wishlist_app.extensions import app, db, bcrypt
from steam_wishlist_app import User, Game, Publisher


"""
Run these tests with the command:
python -m unittest steam_wishlist_app.auth.tests
"""

#################################################
# Setup
#################################################

def create_games():
    a1 = Publisher(name='Team Cherry')
    b1 = Game(
        title='Hallow Knight',
        publish_date=date(1960, 7, 11),
        author=a1
    )
    db.session.add(b1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        # TODO: Write a test for the signup route. It should:
        # - Make a POST request to /signup, sending a username & password
        # - Check that the user now exists in the database
        post_data = {
            'username': 'bob',
            'password': '123'
        }
        self.app.post('/signup', data=post_data)
        
        user = User.query.filter_by(username='bob').first()
        self.assertIsNone(user)

    def test_signup_existing_user(self):
        # TODO: Write a test for the signup route. It should:
        # - Create a user
        # - Make a POST request to /signup, sending the same username & password
        # - Check that the form is displayed again with an error message
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.post('/signup', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('That username is taken. Please choose a different one.', response_text)

    def test_login_correct_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        # - Make a POST request to /login, sending the created username & password
        # - Check that the "login" button is not displayed on the homepage
        create_user()
        post_data = {
            'username': 'me1',
            'password': 'password'
        }
        response = self.app.get('/login', data=post_data)
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertNotIn('login', response_text)

    def test_login_nonexistent_user(self):
        # TODO: Write a test for the login route. It should:
        # - Make a POST request to /login, sending a username & password
        # - Check that the login form is displayed again, with an appropriate
        #   error message
        post_data = {
            'username': 'Bobby',
            'password': '9000'
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn('No user with that username. Please try again.', response_text)

    def test_login_incorrect_password(self):
        # TODO: Write a test for the login route. It should:
        # - Create a user
        # - Make a POST request to /login, sending the created username &
        #   an incorrect password
        # - Check that the login form is displayed again, with an appropriate
        #   error message
        post_data = {
            'username': 'me1',
            'password': 'incorrect password'
        }
        response = self.app.post('/login', data=post_data)
        response_text = response.get_data(as_text=True)
        self.assertIn("Password doesn't match. Please try again.", response_text)

    def test_logout(self):
        # TODO: Write a test for the logout route. It should:
        # - Create a user
        # - Log the user in (make a POST request to /login)
        # - Make a GET request to /logout
        # - Check that the "login" button appears on the homepage
        create_user()
        post_data = {
            'username' : 'me1',
            'password' : 'password'
        }
        self.app.post('/login', data=post_data)
        self.app.get('/logout')
        response = self.app.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('login', response_text)