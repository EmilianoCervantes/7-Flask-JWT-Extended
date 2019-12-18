'''
La habilidad de insertar información (objetos) en la tabla user
'''
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


# Recuperar info de los usuarios y borrarlos
class User(Resource):

    @classmethod
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return { 'message': 'No se encontró al usario' }, 404

    @classmethod
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_user()
            return { 'message': 'Usuario borrado exitosamente' }
        return { 'message': 'El usuario ya fue borrado o no existía' }, 404
