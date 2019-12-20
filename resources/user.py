'''
La habilidad de insertar información (objetos) en la tabla user
'''
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_claims

from models.user import UserModel

# _variable significa que es privada en python
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    required=True,
    type=str,
    help='Username no puede estar vacío'
)
_user_parser.add_argument(
    'password',
    required=True,
    type=str,
    help='Campo password no puede estar vacío'
)


# Crear nuevos usuarios y agregarlos a la BD
class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return { 'message': 'Ese usuario ya existe' }, 400

        # user = UserModel( data['username'], data['password'] ) # versión 1
        user = UserModel( **data ) # versión 2
        user.update_and_insert_users()

        return { 'message': 'Usuario creado exitosamente' }, 201


# Recuperar info de los usuarios y borrarlos
class User(Resource):

    @jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return { 'message': 'No se encontró al usario' }, 404

    @classmethod
    def delete(self, user_id):
        '''
            Uso de jwt claims.
            Que no se pueda borrar a un admin.
        '''
        # claims = get_jwt_claims()
        # if not claims['is_admin']:
        #     return { 'message': 'Debes ser admin' }
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_user()
            return { 'message': 'Usuario borrado exitosamente' }
        return { 'message': 'El usuario ya fue borrado o no existía' }, 404

        # return { 'message': 'Debes ser admin' }, 401


# Emplear flask_jwt_extended
class UserLogin(Resource):
    """Toma user y pass y verifica que sean correctos"""

    def post(self):
        # get datos del parser
        data = _user_parser.parse_args()
        # encontrar el user en la bd
        user = UserModel.find_by_username(data['username'])
        # checar el password
        # Lo que solía hacer la func authenticate()
        if user and safe_str_cmp(user.password, data['password']):
            # crear access Token
            # create_access_token(identidad) es parte de flask_jwt_extended
            # fresh=True es para token refreshing
            access_token = create_access_token(identity=user.id, fresh=True)
            # crear Refresh Token
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return { 'message': 'No se ingresaron credenciales correctas' }, 401
