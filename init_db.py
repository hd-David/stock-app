from model import Base, engine

# This line is the "Table Builder"
# It looks at your User, Address, and Portfolio classes and builds them in MariaDB
print("Building tables...")
Base.metadata.create_all(bind=engine)
print("Tables 'user', 'address', and 'portfolio' are now live in finance_app!")
