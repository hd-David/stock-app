from wtforms.validators import * #DataRequired,EqualTo, Email
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import * #StringField, BooleanField,PasswordField, SubmitField, EmailField, IntegerField, FloatField
from flask_wtf import FlaskForm
import model

session_db = model.dbconnect()
User = model.User()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password',message='Passwords must match.')])
    #submit = SubmitField('Register')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    def validate_username(self, username):
        user = session_db.query(User).filter(User.username == form.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = session_db.query(User).filter(User.email == form.email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuoteForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired()])
    number_of_shares = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Get Qoute")