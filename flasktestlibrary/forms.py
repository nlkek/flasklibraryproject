# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, StringField, RadioField, SelectField
from wtforms.validators import Required, DataRequired
import models


class LoginForm(Form):
    login = StringField(u'Введите логин', validators=[Required()])
    password = PasswordField(u'Введите пароль', validators=[Required()])


class RegistrationForm(Form):
    login = StringField(u'Введите логин', validators=[Required()])
    password = PasswordField(u'Введите пароль', validators=[Required()])
    confirm_password = PasswordField(u'Повторите пароль', validators=[Required()])


class SearchForm(Form):
    search_radio = RadioField('search', choices=[('book',u'Искать по названию книги'), ('author', u'Искать по автору')], default='book')
    search_attr = StringField(u'Введите название книги или имя автора', validators=[Required()])


class AddFormBook(Form):
    name = StringField(u'Введите название книги', validators=[Required()])


class DeleteFormBook(Form):
    list_of_obj = SelectField(u'Выберите книгу', coerce=int, validators=[Required()])


class AddFormAuthor(Form):
    name = StringField(u'Введите имя автора', validators=[Required()])


class DeleteFormAuthor(Form):
    list_of_obj = SelectField(u'Выберите автора', coerce=int, validators=[Required()])


class BookEditForm(Form):
    list_of_books = SelectField(u'Выберите книгу', coerce=int, validators=[Required()])
    list_of_authors = SelectField(u'Выберите автора', coerce=int, validators=[Required()])

