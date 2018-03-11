from init import app
from flask import render_template, flash, redirect, url_for
from forms import LoginForm
from models import User, Book
from init import dbs
from flask_login import login_user
from init import login_manager
from flask.ext.login import login_required, current_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))


@app.route("/settings")
@login_required
def settings():
    return str(current_user.get_id())

@app.route('/')
@app.route('/index')
def index():

    users = {'nickname': 'main admin'}
    books = [
        {
            'author': { 'nickname': 'main admin' },
            'book': 'book1'
        },
        {
            'author': {'nickname': 'user'},
            'book': 'book2'
        }
    ]

    title = 'test'
    return render_template('index.html',
                           user=users,
                           title=title,
                           books=books)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(
            login=form.login.data,
            password=form.password.data
        )
        dbs.session.add(user)
        dbs.session.commit()

        login_user(user)
        flash('Registration successful: ' + form.login.data)
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Logged in as:' + form.login.data)
            return redirect(url_for('index'))
        elif user:
            flash('wrong pass')
        else:
            flash('no such user')
    return render_template('login.html',
                           form=form)

@app.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    books = Book.query.all()
    return render_template('books.html',
                           books=books,
                           user=current_user.login)