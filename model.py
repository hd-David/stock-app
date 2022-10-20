from sqlalchemy import Boolean, Column, MetaData, create_engine, DateTime, ForeignKey, Integer, String, Float,UniqueConstraint
from sqlalchemy.orm import sessionmaker,relation
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64) ,index=True, unique=True)
    password_hash = Column(String(64))
    email = Column(String(64), unique=True)
    cash = Column(Float)
    

# database connection
def dbconnect():
    engine = create_engine("sqlite:///finance.db", connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()