import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT # JWT is Jason Web Token

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList # obs: I need to import along/beyond other reasons, because sqlalchemy need to see the class taht will be create in dadtabase

app = Flask(__name__) # It's a special variable that gets as value the string "__main__" when you’re executing the script
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL','sqlite:///data.db') # connection with system variable (heroku system as well) adn if don't find it it will run 'sqlite:///data.db'. So, in my case, I don't have 'DATABASE_URL' defined locally, but heroku has and, because of that, I can run sqlite locally and postgres in heroku
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # modification necessary to config my db
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # create an endpoint '/auth'

# I dind't need put decorator reoute, so I just followed the example
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


# With the code bellow we can import app now without run the app. The app will run if it is the 'main'
if __name__ == "__main__": # That means the if conditional statement is satisfied and the app.run() method will be executed. This technique allows the programmer to have control over script’s behavior.
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True) # I can put debug=True to see erros
    # I didn't need put port=5000, because is default, but it seems understandable
