import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# (Variable de entorno, Default_Value)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///section4.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Developer.2019@udemyflaskseccion9.cnnhekwxtydc.us-east-2.rds.amazonaws.com/udemyflaskseccion9'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'lo_que_sea'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import database
    database.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
