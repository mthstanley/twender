from flask import Flask
from flask_bootstrap import Bootstrap

from config import config

app = Flask(__name__)
app.config.from_object(config['development'])
Bootstrap(app)

from . import views
