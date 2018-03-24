# -*- coding: utf-8 -*-
from init import app
from flask import render_template, flash, redirect, url_for, request, g
from forms import LoginForm, SearchForm, BookEditForm, AddFormBook, DeleteFormBook, AddFormAuthor, DeleteFormAuthor, RegistrationForm
from models import User, Book, Author
from init import dbs
from flask_login import login_user
from init import login_manager
from flask.ext.login import login_required, current_user, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html', user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('logged out')
    return redirect(url_for('index'))


@app.route("/settings")
@login_required
def settings():
    flash(current_user.get_id())
    return redirect(url_for('index'))


@app.route('/library')
def library():
    title = 'test'
    books = Book.query.all()
    return render_template('library.html',
                           title=title,
                           books=books,
                           user=current_user)


@app.route('/book/<param>')
def book(param):
    current_book = Book.query.get(param)
    return render_template('book.html', book=current_book, user=current_user)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(login=form.login.data).first():
            flash(u'Пользователь с таким логином уже существует')
            return redirect(url_for('register'))
        if form.password.data != form.confirm_password.data:
            flash(u'Пароли не совпадают')
            return redirect(url_for('register'))
        user = User(
            login=form.login.data,
            password=form.password.data
            )
        dbs.session.add(user)
        dbs.session.commit()
        login_user(user)
        flash(form.login.data + u', вы успешно зарегистрировались')
        return redirect(url_for('index'))
    return render_template('registration.html',
                           form=form,
                           user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(form.login.data + u', вы успешно авторизовались')
            return redirect(url_for('index'))
        elif user:
            flash('Неверный пароль')
        else:
            flash('Пользователя с таким логином не существует')
    return render_template('login.html',
                           form=form,
                           user=current_user)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.search_radio.data == 'book':
            books = Book.query.filter(Book.bookname.contains(form.search_attr.data)).all()
            if not books:
                flash(u"Нет такой книги")
            return render_template('search.html',
                                   form=form,
                                   user=current_user,
                                   books=books)
        else:
            authors = Author.query.filter(Author.authorname.contains(form.search_attr.data)).all()
            if not authors:
                flash(u"Нет такого автора")
            return render_template('search.html',
                                   form=form,
                                   user=current_user,
                                   authors=authors)
    return render_template('search.html',
                           form=form,
                           user=current_user)


@app.route("/bookpreedit")
def bookpreedit():
    return render_template('bookpreedit.html', user=current_user)


@app.route("/authorpreedit")
def authorpreedit():
    return render_template('authorpreedit.html', user=current_user)


@app.route("/editbook", methods=['GET', 'POST'])
def bookedit():
    form = BookEditForm()
    form.list_of_books.choices = [(book.id, book.bookname) for book in Book.query.all()]
    form.list_of_authors.choices = [(author.id, author.authorname) for author in Author.query.all()]
    book = Book.query.all()[0]
    if request.method == 'POST':
        if request.form['submit'] == u'Показать авторский состав выбранной книги':
            book = Book.query.get(form.list_of_books.data)
            return render_template('editing.html',
                                   form=form,
                                   user=current_user,
                                   book=book)
        if request.form['submit'] == u'Добавить выбранного автора в авторский состав выбранной книги':
            author = Author.query.get(form.list_of_authors.data)
            book = Book.query.get(form.list_of_books.data)
            book.authors.append(author)
            dbs.session.add(book)
            dbs.session.commit()
            return render_template('editing.html',
                                   form=form,
                                   user=current_user,
                                   book=book)
        if request.form['submit'] == u'Удалить выбранного автора из авторского состава выбранной книги':
            author = Author.query.get(form.list_of_authors.data)
            book = Book.query.get(form.list_of_books.data)
            if author in book.authors:
                book.authors.remove(author)
                dbs.session.add(book)
                dbs.session.commit()
                return render_template('editing.html',
                                       form=form,
                                       user=current_user,
                                       book=book)
    return render_template('editing.html',
                           form=form,
                           user=current_user,
                           book=book)


@app.route("/editbook1", methods=['GET', 'POST'])
def authoredit():
    pass


@app.route("/addbook", methods=['GET', 'POST'])
def addbook():
    form = AddFormBook()
    if form.validate_on_submit():
        if Book.query.filter_by(bookname=form.name.data).first():
            flash(u'Эта книга уже есть в библиотеке')
            return redirect(url_for("addbook"))
        book = Book(bookname=form.name.data)
        dbs.session.add(book)
        dbs.session.commit()
        flash(u'Книга:%s была добавлена в библиотеку' % book.bookname)
        return redirect(url_for("addbook"))
    return render_template('addbook.html',
                           form=form,
                           user=current_user)


@app.route("/deletebook", methods=['GET', 'POST'])
def deletebook():
    form = DeleteFormBook()
    form.list_of_obj.choices = [(book.id, book.bookname) for book in Book.query.all()]
    if request.method == 'POST':
        if request.form['submit'] == u'Удалить книгу':
            book = Book.query.get(form.list_of_obj.data)
            dbs.session.delete(book)
            dbs.session.commit()
            flash(u'Книга:%s была удалена из библиотеки' % book.bookname)
            return redirect(url_for('deletebook'))
        if request.form['submit'] == u'Показать авторский состав выбранной книги':
            book = Book.query.get(form.list_of_obj.data)
            return render_template('deletebook.html',
                                   form=form,
                                   user=current_user,
                                   book=book)
    return render_template('deletebook.html',
                           form=form,
                           user=current_user)


@app.route("/addauthor", methods=['GET', 'POST'])
def addauthor():
    form = AddFormAuthor()
    if form.validate_on_submit():
        if Author.query.filter_by(authorname=form.name.data).first():
            flash(u'Этот автор уже есть в общем списке авторов')
            return redirect(url_for("addauthor"))
        author = Author(authorname=form.name.data)
        dbs.session.add(author)
        dbs.session.commit()
        flash(u'Автор:%s был добавлен в общий список авторов.' % author.authorname )
        return redirect(url_for("addauthor"))
    return render_template('addauthor.html',
                           form=form,
                           user=current_user)


@app.route("/deleteauthor", methods=['GET', 'POST'])
def deleteauthor():
    form = DeleteFormAuthor()
    form.list_of_obj.choices = [(author.id, author.authorname) for author in Author.query.all()]
    if request.method == "POST":
        if request.form['submit'] == u'Удалить автора':
            author = Author.query.get(form.list_of_obj.data)
            dbs.session.delete(author)
            dbs.session.commit()
            return redirect(url_for('deleteauthor'))
        if request.form['submit'] == u'Показать показать книги с этим автором':
            author = Author.query.get(form.list_of_obj.data)
            return render_template('deleteauthor.html',
                                   form=form,
                                   user=current_user,
                                   author=author)
    return render_template('deleteauthor.html',
                           form=form,
                           user=current_user)



