
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