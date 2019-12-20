import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
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
# app.secret_key ≠ app.config['JWT_SECRET_KEY']
# app.config['JWT_SECRET_KEY'] se puede añadir, para tener dos llaves diferentes
api = Api(app)

@app.before_first_request
def create_tables():
    database.create_all()

# jwt = JWT(app, authenticate, identity) # /auth
jwt = JWTManager(app) # NO crea /auth, lo debemos crear nosotros mismos

# Peticiones de los usuarios, tiene que pasar a fuerza identity
# la funcion nombre_que_sea(identity)
@jwt.user_claims_loader # Hace el link con JWTManager()
def add_claims_to_jwt(identity):
    '''Se corre para saber si hay que agregar info extra a nuestro jwt'''
    # Porque en user.UserLogin() pasamos user.id como identity
    # Aquí será igual
    if identity == 1: # Está hardcodeado, la prox mejor lee de BD
        return { 'is_admin': True }
    return { 'is_admin': False }

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import database
    database.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
