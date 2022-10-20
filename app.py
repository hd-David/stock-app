import os
from flask_wtf import FlaskForm
from flask import Flask, flash, redirect, render_template,session, request, url_for
from flask_session import Session
from helpers import apology, login_required, lookup, usd
from create import register_user
from model import User, dbconnect
import forms
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
# pk_ab85953ba81448f28be52d6aa72f4a4b
# Configure application

app = Flask(__name__)

session_db = dbconnect()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
bootstrap = Bootstrap(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session_db to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
SECRET_KEY = os.urandom(64)
app.config['SECRET_KEY'] = SECRET_KEY
Session(app)


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return "username missing", 403

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "password missing", 403

        # Query database for username
        user = session_db.query(User).filter(User.username == request.form.get("username")).one()

        # Ensure username exists and password is correct
        if user is None or not user.check_password_hash(request.form.get("password")):
            return "invalid username or password", 403

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    return apology("TODO")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


@app.route("/register", methods=["GET","POST"])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = session_db.query(User).filter(User.username == form.username.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password.data)
            user = register_user({'username':form.username.data, 'password':hashed_password, 
            'cash':form.cash.data, 'email':form.email.data})
            session_db.add(user)
            session_db.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form,)
            
        
if __name__ == '__main__':
    app.run(debug=True)