from init import app
from flask import render_template, flash, redirect, url_for
from forms import LoginForm

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign in',
                           form=form)