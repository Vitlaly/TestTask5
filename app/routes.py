from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Book, Author


@app.route('/')
@app.route('/index')
@login_required
def index():
    books = db.session.query(Book).all()
    author= db.session.query(Author).all()
    user= db.session.query(User).first()
    return render_template("index.html", books=books, author=author, user=user)

@app.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        db.session.add(newBook)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('newBook.html')


# Эта функция позволит нам обновить книги и сохранить их в базе данных.
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name1'] or request.form['name']:
            editedBook.title = request.form['name1']
            editedBook.author = request.form['name']
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return render_template('editBook.html', book=editedBook)


# Эта функция для удаления книг
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        db.session.delete(bookToDelete)
        db.session.commit()
        return redirect(url_for('index', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
