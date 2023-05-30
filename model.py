from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

Base = declarative_base()


# Define the user model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password_hash = Column(String(64))
    cash = Column(Float, default=10000.00)
    time_stamp = Column(DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserDetails(Base):
    __tablename__ = 'user_details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)


# Define the cash model
class Cash(Base):
    __tablename__ = 'cash'

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    debit = Column(Float, nullable=False)
    credit = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    trans_id = Column(String)


class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    holdings = Column(Integer)
    order_price = Column(Float)
    date = Column(DateTime)


class UserPortfolio(Base):
    __tablename__ = 'user_portfolio'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'))


# Database connection
def dbconnect():
    engine = create_engine("sqlite:///finance.db", connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


# Create session
session = dbconnect()

user_portfolios = session.query(UserPortfolio).filter_by(user_id=1).all()
portfolios = []
for user_portfolio in user_portfolios:
    portfolio = session.query(Portfolio).filter_by(id=user_portfolio.portfolio_id).first()
    portfolios.append(portfolio)
