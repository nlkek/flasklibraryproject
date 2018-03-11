from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, StringField
from wtforms.validators import Required


class LoginForm(Form):
    login = StringField('login', validators=[Required()])
    password = PasswordField('pass', validators=[Required()])
    #remember_me = BooleanField('remember_me', default = False)