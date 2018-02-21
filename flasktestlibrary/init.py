from flask import Flask

app = Flask('__main__')
app.config.from_object('config')
import views