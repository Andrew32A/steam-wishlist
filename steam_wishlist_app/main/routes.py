"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from steam_wishlist_app.models import Book, Author, Genre, User
from steam_wishlist_app.main.forms import BookForm, AuthorForm, GenreForm

# Import app and db from events_app package so that we can run app
from steam_wishlist_app.extensions import app, db, bcrypt

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

def create_books():
    a1 = Author(name='FromSoftware')
    b1 = Book(
        title='Bloodborne',
        publish_date=date(2015, 3, 24),
        author=a1
    )
    db.session.add(b1)

    a2 = Author(name='Team Cherry')
    b2 = Book(title='Hollow Knight', author=a2)
    db.session.add(b2)
    db.session.commit()
# create_books()


@main.route('/')
def homepage():
    all_books = Book.query.all()
    all_users = User.query.all()
    return render_template('home.html',
        all_books=all_books, all_users=all_users)


@main.route('/create_book', methods=['GET', 'POST'])
@login_required
def create_book():
    form = BookForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_book = Book(
            title=form.title.data,
            publish_date=form.publish_date.data,
            author=form.author.data,
            audience=form.audience.data,
            genres=form.genres.data
        )
        db.session.add(new_book)
        db.session.commit()

        flash('New game was added successfully.')
        return redirect(url_for('main.book_detail', book_id=new_book.id))
    return render_template('create_book.html', form=form)


@main.route('/create_author', methods=['GET', 'POST'])
@login_required
def create_author():
    form = AuthorForm()
    if form.validate_on_submit():
        new_author = Author(
            name=form.name.data,
            biography=form.biography.data
        )
        db.session.add(new_author)
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


@main.route('/book/<book_id>', methods=['GET', 'POST'])
def book_detail(book_id):
    book = Book.query.get(book_id)
    form = BookForm(obj=book)
    
    # if form was submitted and contained no errors
    if form.validate_on_submit():
        book.title = form.title.data
        book.publish_date = form.publish_date.data
        book.author = form.author.data
        book.audience = form.audience.data
        book.genres = form.genres.data

        db.session.commit()

        flash('Game was updated successfully.')
        return redirect(url_for('main.book_detail', book_id=book_id))

    return render_template('book_detail.html', book=book, form=form)


@main.route('/profile/<username>')
def profile(username):
    all_books = Book.query.all()

    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user, all_books=all_books)


@main.route('/favorite/<book_id>', methods=['POST'])
@login_required
def favorite_book(book_id):
    book = Book.query.get(book_id)
    if book in current_user.favorite_books:
        flash('Game already in wishlist.')
    else:
        current_user.favorite_books.append(book)
        db.session.add(current_user)
        db.session.commit()
        flash('Game added to wishlist.')
    return redirect(url_for('main.book_detail', book_id=book_id))


@main.route('/unfavorite/<book_id>', methods=['POST'])
@login_required
def unfavorite_book(book_id):
    book = Book.query.get(book_id)
    if book not in current_user.favorite_books:
        flash('Game not in wishlist.')
    else:
        current_user.favorite_books.remove(book)
        db.session.add(current_user)
        db.session.commit()
        flash('Game removed from wishlist.')
    return redirect(url_for('main.book_detail', book_id=book_id))
