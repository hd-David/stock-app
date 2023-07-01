from sqlalchemy import create_engine, insert, update, delete, select, UniqueConstraint,DateTime, join
from sqlalchemy import Table, Column,Integer, String, ForeignKey,Numeric, MetaData,Float, func 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import  Mapped,mapped_column, DeclarativeBase, relationship
import sqlite3
from typing import Optional, List
from sqlalchemy.orm import Session



# Now you can use the sqlite3 module and its functionality in your code

class Base(DeclarativeBase):
    pass

print(Base)
# Define the user model
class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    full_names = mapped_column(String(64))
    username = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    password_hash = mapped_column(String(100))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
   #user: Mapped["Portfolio"] = relationship(back_populates="user")
    cash: Mapped[int] = mapped_column(insert_default=10000)
    email: Mapped[str] = mapped_column(String, nullable=False)
  
 
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
 
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    emaill: Mapped[str]
    user: Mapped["User"] = relationship(back_populates="addresses")
 


# class Portfolio(Base):
#     __tablename__ = 'portfolio'
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user: Mapped["User"] = relationship(back_populates="portfolio")
#     symbol = Column(String)
#     quantity = Column(Integer)
#     price = Column(Float)


# database connection
def dbconnect():
   
    engine = create_engine('sqlite:///finance.db')
    Base.metadata.create_all(bind=engine)

    print(engine)
    with Session(engine) as session:
        return session

print(dbconnect())