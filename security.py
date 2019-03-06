from werkzeug.security import safe_str_cmp # this is to compare string safely in python 2.7, but works well in all version python
from models.user import UserModel

def authenticate(username,password):
    user = UserModel.find_by_username(username)
    # if user and user.password == password: # compare string normaly in python 3
    if user and safe_str_cmp(user.password,password): # to campare string safely in python 2.7, but works in all codes as well
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
