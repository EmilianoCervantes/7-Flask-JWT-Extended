import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///section7.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Developer.2019@udemyflaskseccion9.cnnhekwxtydc.us-east-2.rds.amazonaws.com/udemyflaskseccion9'
# Agregado por si JWT lanza un error
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'lo_que_sea'
api = Api(app)

@app.before_first_request
def create_tables():
    database.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    from db import database
    database.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
