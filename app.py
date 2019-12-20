import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///section7.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
# Agregado por si JWT lanza un error
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
# Tipos de tokens que se pueden bloquear
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'lo_que_sea'
# app.secret_key != app.config['JWT_SECRET_KEY']
# app.config['JWT_SECRET_KEY'] se puede añadir, para tener dos llaves diferentes
api = Api(app)

@app.before_first_request
def create_tables():
    database.create_all()

# jwt = JWT(app, authenticate, identity) # /auth
jwt = JWTManager(app) # NO crea /auth, lo debemos crear nosotros mismos

""""""""""""""""""""""""""""""
"""Configuraciones jwt start"""
""""""""""""""""""""""""""""""

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

# Cuando flask_jwt_extended se de cuenta que
# el jwt token ha expirado, llamará a esta función.
@jwt.expired_token_loader
def token_expirado_callback():
    return {
        'description': 'El token ha expirado',
        'error': 'token_expirado'
    }, 401

# Cuando el token que se recibe no es un JWT
@jwt.invalid_token_loader
def token_invalido_callback(callback = None):
    return {
        'description': 'El token ha expirado',
        'error': 'invalid_token'
    }, 401

# Cuando ni siquiera se mande un jwt
@jwt.unauthorized_loader
def token_no_autorizado_callback():
    return {
        'description': 'No se envió un token',
        'error': 'token_unauthorized'
    }, 401

# Cuando se recibe un non-fresh token
@jwt.needs_fresh_token_loader
def token_necesita_refresh_callback():
    return {
        'description': 'Se necesita un refresh',
        'error': 'token_unfresh'
    }, 401

# Decir que un token ya no es válido
# Ej: logout -> el token se manda a revoked token list
@jwt.revoked_token_loader
def token_revocado_callback():
    return {
        'description': 'El token fue revocado',
        'error': 'token_revoked'
    }, 401

# Para indicar qué es un elemento en blacklist y qué no
# True si el token está en el blacklist
# Irá al @revoked_token_loader() y dirá que NEL de acceso
@jwt.token_in_blacklist_loader
def checar_token_en_blacklist(decrypted_token):
    # return decrypted_token['identity'] in BLACKLIST
    return decrypted_token['jti'] in BLACKLIST

""""""""""""""""""""""""""""""
"""Configuraciones jwt end"""
""""""""""""""""""""""""""""""

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/signup')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from db import database
    database.init_app(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
