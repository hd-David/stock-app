
# # Import the necessary modules
# from sqlalchemy import func

# # Define the subquery
# subquery = session.query(Transaction.c_id,
#                          Transaction.user_id,
#                          func.sum(Transaction.quantity * Transaction.price).label('total_cost'),
#                          func.sum(Transaction.quantity).label('total_quantity')
#                          ) \
#               .join(Company) \
#               .join(User) \
#               .filter(User.id==1) \
#               .group_by(Transaction.c_id, Transaction.user_id)

# # Use the subquery in the outer query
# results = session.query(Company.name,
#                         Company.symbol,
#                         User.username,
#                         subquery.c.total_cost,
#                         subquery.c.total_quantity
#                         ) \
#              .join(subquery, Company.id==subquery.c.c_id) \
#              .join(User, User.id==subquery.c.user_id) \
#              .order_by(Company.name)






# def generate_payslip(array_of_objects):
#   current_month = get_date().month
#   current_year = get_date().year

#   for row_no in range(1, len(array_of_objects) + 1):
#     payslip_template = urls()["payslipTemplate"]
#     payslips_details_folder = outputDriveFolder

#     # Creating a copy of the salary template
#     payslip_file = payslip_template.make_copy(payslips_details_folder)
#     payslip = DocumentApp.open_by_id(payslip_file.get_id())
#     payslip_content = payslip.get_body()

#     # Substituting variables from the data coming from the sheet named source
#     # into the original salary template.
#     payslip_content.replace_text("NAXX", array_of_objects[row_no].first_name + " " + array_of_objects[row_no].last_name)
#     payslip_content.replace_text("DESXX", array_of_objects[row_no].designation)
#     payslip_content.replace_text("MONXXX", str(get_date().month + 1) + " " + str(get_date().year))
#     payslip_content.replace_text("BASICXX", array_of_objects[row_no].gross_pay)
#     payslip_content.replace_text("NAPSAXX", array_of_objects[row_no].napsa_value)
#     payslip_content.replace_text("PAYEX", array_of_objects[row_no].paye_value)
#     payslip_content.replace_text("NHIMAXX", array_of_objects[row_no].nhima_value)
#     payslip_content.replace_text("TDXXXX", array_of_objects[row_no].total_deduction)
#     payslip_content.replace_text("NETPAYXX", array_of_objects[row_no].net_pay)
#     payslip_content.replace_text("ACCXX", array_of_objects[row_no].bank_account_number)
#     payslip_content.replace_text("BNXX", array_of_objects[row_no].bank_name)
#     payslip_content.replace_text("ADXX", array_of_objects[row_no].branch_name)
#     payslip_content.replace_text("EMPID", array_of_objects[row_no].employee_id)
#     payslip.save_and_close()

#     # Converting the Google Docs payslip template to PDF format and
#     # deleting the copy file.
#     payslip = payslip.get_as(MimeType.PDF)
#     payslip_pdf = payslips_details_folder.create_file(payslip).set_name("Salary_" + array_of_objects[row_no].first_name + " " + array_of_objects[row_no].last_name)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64) ,index=True, unique=True)
    password_hash = Column(String(64))
    email = Column(String(64), unique=True)
    cash = Column(Float)
    time_stamp = Column(DateTime, default=datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Name(Base):
    __tablename__ = 'names'
    name_id = Column(Integer, primary_key=True) 
    first_name = Column(String(30))
    last_name = Column(String(30))               
    user = relation('User', backref='names') 
    user_id = Column(Integer, ForeignKey(User.id))

# class Companies(Base):
#     pass



    # Import the necessary modules
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create the declarative base for the models
Base = declarative_base()




from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('database_url')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    cash = Column(Integer)

class Portfolio(Base):
    __tablename__ = 'portfolios'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    symbol = Column(String)
    holdings = Column(Integer)
    order_price = Column(Integer)
    date = Column(DateTime)

def sell():
    """Sell shares of stock"""

    # Display sell.html when requested
    if request.method == "GET":
        return render_template("sell.html")

    # When Sell Now button press - run our checks then add to database
    if request.method == "POST":

        # Lets get information about the stock code and amount of shares
        symbol = request.form.get("symbol")
        holdings = float(request.form.get("number"))

        # Define the order total (negative number!)
        order_price = -1 * (int(lookup(symbol)["price"]) * (holdings))

        user_dict = session.query(User).filter_by(username=session["user_id"]).first()
        username = user_dict.username

        # Ease of access for current portfolio
        current_portfolio = username+"_portfolio"
        curr_port = session.query(Portfolio).filter_by(username=current_portfolio).all()

        # Current portfolio COPY
        current_copy = username+"_copy"

        # Define the available cash the user has
        available_cash = session.query(User).filter_by(username=username).first().cash

        # Run checks
        # First check: did they enter number of stocks
        if not holdings:
            return apology("please enter the number of stocks you wish to purchase", 400)

        # Second check: did they enter a stock code
        if not symbol:
            return apology("please enter a stock symbol", 400)

        # Third check: did they enter a VALID stock code
        if not lookup(symbol):
            return apology("please enter a valid stock symbol", 400)

        # Fourth check: Did they enter a postive integer amount of stocks
        if holdings < 0:
            return apology("please enter a positive integer of stocks")

        # Fith check: Is selling number less than the amount they own
        # Define current_holdings
        current_holdings_dict = session.query(Portfolio).filter_by(username=current_portfolio, symbol=symbol).first()
        current_holdings = current_holdings_dict.holdings
        if holdings > current_holdings:
            return apology("sorry, you cannot sell more stocks than you own", 400)



# Get user inputs
name = request.form.get('name')
gender = request.form.get('gender')
email = request.form.get('email')
phone = request.form.get('phone')

# Create new user and user_details objects
new_user = User(username=email, cash=1000)
new_user_details = UserDetails(user_id=new_user.id, name=name, gender=gender, email=email, phone=phone)

# Add the new objects to the session
session.add(new_user)
session.add(new_user_details)

# Commit the changes to the database
session.commit()
