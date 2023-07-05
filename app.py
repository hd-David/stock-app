import os
from flask import Flask, flash, redirect, render_template,session, request, url_for
from helpers import *
from create import *
from model import dbconnect, User, Address
from flask_bootstrap import Bootstrap
import forms
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, LoginManager, login_user, logout_user



# pk_cda57eb3533f4aafac734ec7523ac410

# Configure application

app = Flask(__name__, static_folder="static")

login_manager = LoginManager()
login_manager.init_app(app)

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

    # Get the user's ID
    user_id = current_user.id
    print(user_id)
    if request.method == "GET":
        # Retrieve the portfolio data for the user
        portfolio_data = get_portfolio_data(user_id)
        print(portfolio_data[1])
        # Pass the portfolio data to the template for rendering
        return render_template("index.html", stocks=portfolio_data)

    return render_template("index.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")

# User loader function
@login_manager.user_loader
def load_user(user_id):
    # Load and return the User object based on the user_id
    user = session_db.query(User).get(int(user_id))
    return user

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
            return "Invalid username or password", 403

        # Remember which user has logged in
        login_user(user)

        # Redirect the user to the home page or any other desired page
        return redirect("/")

    # User reached route via GET (by clicking a link or via redirect)
    else:
        return render_template("page_login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    logout_user()

    # Redirect user to login form
    return redirect("/login")



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
        print(form.username.data)
        # Check if the full_names or email already exists in the database
        existing_user = session_db.query(User).filter(User.email == form.email.data).first()
        existing_username = session_db.query(User).filter(User.username == form.username.data).first()
        if existing_user is not None and existing_user.email == form.email.data:
            form.email.errors.append('Please email already exist, use a different email address.')
        if existing_username is not None and existing_username.username == form.username.data:
            form.username.errors.append('Please username already exist, use a different username.')
        else:
            try:
                # Create the user object
                hashed_password = generate_password_hash(form.password.data)
                user = User(
                    full_names=form.full_names.data,
                    email=form.email.data,
                    password_hash=hashed_password,
                    username=form.username.data
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
        if result == "Success":
            flash("Stock purchased successfully!", "success")
        else:
            flash(result, "error")
        
        return redirect(url_for('index'))
    
    # Render form for GET request
    return render_template('buy.html')


def buy(symbol, quantity):
    stock_info = lookup(symbol)
    # Check if stock exists
    if stock_info is None:
        return "Invalid symbol"
    
    user = session_db.query(User).get(current_user.id)
    budget = user.cash
    # Check if sufficient funds available
    if stock_info["price"] * float(quantity) > budget:
        return "Insufficient funds"
    
    # Purchase stock
    total_cost = stock_info["price"] * float(quantity)
    user.cash -= total_cost
    
    # Add stock to user's portfolio
    portfolio = Portfolio(user_id=user.id, symbol=symbol, quantity=quantity, price=stock_info["price"])
    session_db.add(portfolio)
    session_db.commit()
   
    return "Success"


def get_portfolio_data(user_id):
    # Retrieve the portfolio for the given user_id
    portfolio = session_db.query(Portfolio).filter_by(user_id=user_id).all()
    print(portfolio)

    # Create an empty list to store the portfolio data
    portfolio_data = []

    # Iterate over each portfolio entry
    for entry in portfolio:
        # Retrieve the stock symbol and quantity from the portfolio entry
        symbol = entry.symbol
        quantity = entry.quantity

        # Use the lookup function to fetch the stock quote data for the symbol
        quote_data = lookup(symbol)

        # If the lookup was successful and quote data is available
        if quote_data:
            # Extract the company name and price from the quote data
            company_name = quote_data["name"]
            price = quote_data["price"]

            # Calculate the total value of the stock holding
            total_value = price * quantity

            # Create a dictionary with the portfolio data for this stock
            stock_data = {
                "symbol": symbol,
                "company_name": company_name,
                "price": price,
                "quantity": quantity,
                "total_value": total_value,
            }

            # Add the stock data to the portfolio_data list
            portfolio_data.append(stock_data)

    # Return the portfolio data
    return portfolio_data

            
        
if __name__ == '__main__':
    app.run(debug=True)