from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.items import Item, ItemList
from resources.store import Store, StoreList
from db import db
import os
import re

# HTTP status codes
# 200 - Success
# 201 - Created
# 202 - Accepted
# 400 - Bad request
# 401 - Not authorised
# 404 - Not found
# 500 - Internal server error



app = Flask(__name__)

# to resolve issue with heroku postgresql connection
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri if uri else 'sqlite:///data.db'
# to disable Flask SQLALCHEMY track modification access
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'loki'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

# To avoid executing the below line during imports 
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=4000, debug=True)


