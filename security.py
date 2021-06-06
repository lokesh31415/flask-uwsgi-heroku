
from models.user import UserModel
from werkzeug.security import safe_str_cmp


# below two functions are used in flask JWT method

# this will be called during login
def authenticate(username, password):
    user = UserModel.fetch_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# this will be called whenever request contains jwt token
def identity(payload):
    user_id = payload['identity']
    return UserModel.fetch_by_id(user_id)


