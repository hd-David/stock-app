from sqlalchemy import *
from sqlalchemy.orm import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
Base = declarative_base()


# Define the user model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64) ,index=True, unique=True)
    password_hash = Column(String(64))
    email = Column(String(64), unique=True)
    cash = Column(Float, default=10000.00)
    time_stamp = Column(DateTime, default=datetime.utcnow)
    name = relationship("Name", back_populates="user")
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Define the name model
class Name(Base):
    __tablename__ = 'names'
    
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email_address = Column(String, nullable=False)
    name_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship('User', back_populates='name')

# Define the company model
class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String, unique=True)
    exchange = Column(String, nullable=False)

# Define the cash model
class Cash(Base):
    __tablename__ = 'cash'
    
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    debit = Column(Float, nullable=False)
    credit = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    trans_id = Column(String)

# Define the transaction model
class Transaction(Base):
    __tablename__ = 'transactions'
    
    trans_id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    ordertype = Column(String, CheckConstraint('ordertype IN ("BUY", "SELL")'))
    c_id = Column(Integer, ForeignKey('companies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


# database connection
def dbconnect():
    engine = create_engine("sqlite:///finance.db", connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()