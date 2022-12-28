from wtforms.validators import * #DataRequired,EqualTo, Email
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import * #StringField, BooleanField,PasswordField, SubmitField, EmailField, IntegerField, FloatField
from flask_wtf import FlaskForm
import model

session_db = model.dbconnect()
User = model.User()

class RegistrationForm(FlaskForm):
    full_names = StringField('Full names',validators=[InputRequired(), Length(min=8, max=80)])
    gender = StringField('Full names',validators=[InputRequired(), Length(min=8, max=80)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    gender = StringField('Gender',validators=[InputRequired(), Length(min=8, max=80)])
    phone = StringField('Phone Number',validators=[InputRequired(), Length(min=8, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',message='Passwords must match.')])
    submit = SubmitField('Register')


# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
#     email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
#     confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
   

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuoteForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired()])
    number_of_shares = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Get Qoute")