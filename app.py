import os, forms
from flask_wtf import FlaskForm
from flask import * #Flask, flash, redirect, render_template,session, request, url_for
from flask_session import Session
from helpers import *
from create import *
from model import *
from flask_bootstrap import Bootstrap
from werkzeug.security import* 
from wtforms.validators import *
from flask_login import current_user
from forms import *

# pk_9dc7d1c4be2544609f4869655eadaf5b

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
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY



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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        pass
    return render_template("index.html")

 
#@app.route("/buy", methods=["GET", "POST"])

portfolio = {}

def buy(symbol, quantity):
    stock_info = lookup(symbol)
    global portfolio
    # Check if stock exists
    if stock_info is None:
        return "Invalid symbol"
    user = session_db.query(User).filter_by(username=User.username).first()
    budget = user.cash
    print(budget)
    # Check if sufficient stock available
    if stock_info["price"] * float(quantity) > budget:
        return "Insufficient funds"

    # Purchase stock
    portfolio[symbol] = quantity
    budget -= stock_info["price"] * float(quantity)
    print(portfolio)
   
    return "The purchase is succesful"


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    form = LoginForm()

    # Forget any user_id
    # session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        entered_username_or_email = request.form.get("username") 
        if not entered_username_or_email:
            return "username missing", 403
        # Ensure password was submitted
        elif not request.form.get("password"):
            return "password missing", 403

        # Query database for username
        user = session_db.query(User).filter((User.username == username) | (User.email == username)).first()

        # Ensure username exists and password is correct
        if user is None or not user.verify_password(request.form.get("password")):
            return "invalid username or password", 403
        print(user.id)
        # Remember which user has logged in
        print(session)
        session["user_id"] = user.id
        print("Session user_id:", session["user_id"])
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("page_login.html", form=form)




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
    global lookup_for_stock
    form = forms.QuoteForm()
    if form.validate_on_submit():
        symbol = form.symbol.data
        quantity = form.number_of_shares.data
        print(symbol, quantity)
        # we check the data user entered
        if not symbol or not quantity:
            return "Missing stock symbol and number of stocks", 400
        # Negative number of stocks
        elif int(quantity) < 0:
            return "Please enters above one or positive  number of stocks", 400

        # Use lookup function to check if stock code is valid
        if not lookup(symbol):
            return "stock code was not found, please enter a valid stock symbol", 400
        else:
            # Display the stock information to the user: Stock code, price, and stock name
            return render_template("quoted.html", name=lookup(symbol)["name"], symbol=lookup(symbol)["symbol"],  price = lookup(symbol)["price"], order_price = (lookup(symbol)["price"] * int(quantity)), quantity=quantity)

    return render_template("quote.html", form=form)



@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_stocks():
  if request.method == 'POST':
    ticker = request.form['ticker']
    quantity = request.form['quantity']
    # perform sell operation
    return render_template('success.html')
  else:
    return render_template('sell_stocks.html', user=current_user)


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        # Check if the username or email exists
        user_name = session_db.query(User).filter(User.email == form.email.data).first()
        email = session_db.query(User).filter(User.email == form.email.data).first()
        if user_name is not None:
            form.username.errors.append('Please use a different username.')
        if email is not None:
            form.email.errors.append('Please use a different email address.')
        if user_name is None and email is None:
            try:
                # Create the user
                hashed_password = generate_password_hash(form.password.data)
                print(hashed_password)
                user = register_user({'password_hash':hashed_password, 'email':form.email.data})
                user_details = UserDetails(name=name)
                print(user.username)
                session_db.add(user)
                session_db.add(user_details)
                session_db.commit()
                flash('you have successfuly registred.')
                return redirect(url_for('login'))
            except Exception as e:
                # Catch any errors that may occur and handle them appropriately
                flash('An error occurred while registering the user: {}'.format(e))
    return render_template('register.html',form=form)



@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy_route():
    if request.method == 'POST':
        # Get user input from form
        symbol = request.form['ticker']
        quantity = request.form['quantity']
        
        # Call buy function
        result = buy(symbol, quantity)
        
        return result
    
    # Render form for GET request
    return render_template('buy.html')


portfolio = {}

def buy(symbol, quantity):
    stock_info = lookup(symbol)
    global portfolio
    # Check if stock exists
    if stock_info is None:
        return "Invalid symbol"
    user = session_db.query(User).filter_by(username=User.username).first()
    budget = user.cash
    # Check if sufficient stock available
    if stock_info["price"] * float(quantity) > budget:
        return "Insufficient funds"

    # Purchase stock
    if symbol in portfolio:
        portfolio[symbol] += quantity
    else:
        portfolio[symbol] = quantity
    budget -= stock_info["price"] * float(quantity)
    print(portfolio)

    # Add stock to database
    new_stock = Portfolio(user_id=user.id, symbol=symbol, quantity=quantity, price=stock_info["price"])
    session_db.add(new_stock)
    session_db.commit()
   
    return redirect("/") 

            
        
if __name__ == '__main__':
    app.run(debug=True)