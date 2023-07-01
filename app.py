import os
from flask import Flask, flash, redirect, render_template,session, request, url_for
from helpers import *
from create import *
from model import dbconnect, User, Address
from flask_bootstrap import Bootstrap
import forms
from sqlalchemy.exc import IntegrityError


# pk_710dfbff83df487e9e7ec13c06466185

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
    user = session_db.query(User).filter_by(full_names=User.full_names).first()
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
    # User reached route via POST (by submitting a form via POST)
    if request.method == "POST":
        username_or_email = request.form.get("username_or_email")
        password_entered = request.form.get("password")

        if username_or_email == "":
            return "Username or email missing", 403
        elif password_entered == "":
            return "Password missing", 403

        # Query the database for the user using the full_names or email
        user = session_db.query(User).filter(User.email == username_or_email).first()

        # Ensure the user exists and the password is correct
        if user is None or not user.verify_password(password_entered):
            return "Invalid full_names or password", 403

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect the user to the home page or any other desired page
        return redirect("/")

    # User reached route via GET (by clicking a link or via redirect)
    else:
        return render_template("page_login.html")



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


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        # Check if the full_names or email already exists in the database
        existing_user = session_db.query(User).filter(User.email == form.email.data).first()
        if existing_user is not None:
            if existing_user.email == form.email.data:
               form.email.errors.append('Please use a different email address.')
        else:
            try:
                # Create the user object
                hashed_password = generate_password_hash(form.password.data)
                user = User(
                    full_names=form.full_names.data,
                    email=form.email.data,
                    password_hash=hashed_password
                )
                # Add the user to the session and commit to the database
                session_db.add(user)
                session_db.commit()

                flash('You have successfully registered.')
                return redirect(url_for('login'))
            except IntegrityError:
                # Handle the case when the full_names or email already exists
                session_db.rollback()
                flash('Username or email already exists. Please choose a different one.')
            except Exception as e:
                # Catch any other errors that may occur and handle them appropriately
                flash('An error occurred while registering the user: {}'.format(e))

    return render_template('register.html', form=form)




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
    user = session_db.query(User).filter_by(full_names=User.full_names).first()
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