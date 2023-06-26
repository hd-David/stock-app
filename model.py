from sqlalchemy import create_engine, insert, update, delete, select, UniqueConstraint,DateTime, join
from sqlalchemy import Table, Column,Integer, String, ForeignKey,Numeric, MetaData,Float, inspect
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Define the user model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64) ,index=True, unique=True)
    email = Column(String, nullable=False)
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
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
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
    user_id = Column(Integer, ForeignKey('users.id'))
    symbol = Column(String)
    quantity = Column(Integer)
    price = Column(Float)


# class UserPortfolio(Base):
#     __tablename__ = 'user_portfolio'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     portfolio_id = Column(Integer, ForeignKey('portfolio.id'))

# user_portfolios = session.query(UserPortfolio).filter_by(user_id=1).all()
# portfolios = []
# for user_portfolio in user_portfolios:
#     portfolio = session.query(Portfolio).filter_by(id=user_portfolio.portfolio_id).first()
#     portfolios.append(portfolio)


# database connection
def dbconnect():
    engine = create_engine("sqlite:///finance.db", connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    db_session = sessionmaker(bind=engine)
    return db_session()