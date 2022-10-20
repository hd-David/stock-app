from model import dbconnect, User

def register_user(user_dict):
    user = User()
    user.username = user_dict['username']
    user.password_hash = user_dict['password']
    user.cash = user_dict['cash']
    user.email = user_dict['email']
    return user