from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, StringField, RadioField, SelectField
from wtforms.validators import Required, DataRequired
import models


class LoginForm(Form):
    login = StringField('login', validators=[Required()])
    password = PasswordField('pass', validators=[Required()])


class SearchForm(Form):
    search_radio = RadioField('search', choices=[('book', 'search by bookname'), ('author', 'search by author')], default='book')
    search_attr = StringField('search_attr', validators=[Required()])


class AddForm(Form):
    name = StringField('name', validators=[Required()])


class DeleteForm(Form):
    list_of_obj = SelectField('objs', coerce=int, validators=[Required()])


class BookEditForm(Form):
    list_of_books = SelectField('book', coerce=int, validators=[Required()])
    list_of_authors = SelectField('author', coerce=int, validators=[Required()])

