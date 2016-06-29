"""
forms.py

contains form classes for form objects used in twender 
web application
"""

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
