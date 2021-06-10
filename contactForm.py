from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
import email_validator

class ContactForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Email', validators=[DataRequired(), Email()])
  message = TextAreaField('Message', validators=[DataRequired(), Length(min=2)])
  submit = SubmitField('Send Message')

