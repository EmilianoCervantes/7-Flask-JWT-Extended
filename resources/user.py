'''
La habilidad de insertar información (objetos) en la tabla user
'''

import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, type=str, help='Username no puede estar vacío')
    parser.add_argument('password', required=True, type=str, help='Campo password no puede estar vacío')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Ese usuario ya existe'}, 400

        # user = UserModel( data['username'], data['password'] ) # versión 1
        user = UserModel( **data ) # versión 2
        user.update_and_insert_users()

        return {'message': 'Usuario creado exitosamente'}, 201
