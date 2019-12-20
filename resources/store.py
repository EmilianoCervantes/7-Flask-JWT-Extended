from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.store import StoreModel


class StoreList(Resource):
    @jwt_required
    def get(self):
        return { 'stores': [ store.json() for store in StoreModel.find_all() ] }


class Store(Resource):
    @jwt_required
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return { 'message': None }, 404

    @jwt_required
    def post(self, name):
        if StoreModel.find_by_name(name):
            return { 'message': f'Ya existe {name}' }, 400

        store = StoreModel(name)
        try:
            store.update_and_insert_stores()
        except Exception as e:
            return { 'message': 'Ocurrió un error interno' }, 500

        return store.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if claims['is_admin']:
            store = StoreModel.find_by_name(name)
            if store:
                store.delete_store()
                return { 'message': f'{name} fue borrado exitosamente' }, 200

            return { 'message': f'{name} no se encontró o ya fue borrado' }, 400

        return { 'message': 'Debes ser admin' }, 401
