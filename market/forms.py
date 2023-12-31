from collections.abc import Mapping, Sequence
import re
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Regexp
from market import User



class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already taken!')

    def validate_email_adress(self, email_to_check):
        email_adress = User.query.filter_by(email_adress=email_to_check.data).first()
        if email_adress:
            raise ValidationError('Email Address already taken!')

    username = StringField(label='User Name:', validators=[Length(min = 2, max = 30), DataRequired()])
    email_adress = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user == None:
            raise ValidationError('Username already taken!')

    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label=' Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')

class StopSellingForm(FlaskForm):
    submit = SubmitField(label='Remove Offer!')

class CreateItemForm(FlaskForm):
    
    name = StringField(label='Name:', validators=[Length(min = 2, max = 30), DataRequired(), Regexp(re.compile(r"^[\w\-!%#@]{2,}$"))])
    price = IntegerField(label='Price', validators=[DataRequired()])
    description = StringField(label='Description:', validators=[Length(min = 2, max = 1024), DataRequired()])
    submit = SubmitField(label='Create Item')
