
from models.user import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required=True,
        help="username cannot be empty!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="password cannot be empty!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel(data['username'], data['password'])
        if user and UserModel.fetch_by_username(user.username):
            return {"message": "user with the username '{}' already exist.".format(user.username)}, 400
        try:
            user.save_to_db()
            return {"message": "user registered successfully"}, 201
        except:
            return {"message": "internal server error"}, 500
        