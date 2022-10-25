from sqlalchemy import Boolean, Column, MetaData, create_engine, DateTime, ForeignKey, Integer, String, Float,UniqueConstraint
from sqlalchemy.orm import sessionmaker,relation
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
Base = declarative_base()

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


# database connection
def dbconnect():
    engine = create_engine("sqlite:///finance.db", connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()