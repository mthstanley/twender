"""
forms.py

contains form classes for form objects used in twender
web application
"""
from flask import current_app
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

from tweepy import TweepError

class SearchForm(Form):
    username = StringField('username', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        try:
            self.user = current_app.tweepy_api.get_user(self.username.data)
            return True
        except TweepError as error:
            self.username.errors.append("Ooops! I couldn't find them.")
            return False

