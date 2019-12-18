from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel

class StoreList(Resource):
    @jwt_required()
    def get(self):
        return { 'stores': [ store.json() for store in StoreModel.query.all() ] }


class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return { 'name': None }, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return { 'message': f'Ya existe {name}' }, 400

        store = StoreModel(name)
        try:
            store.update_and_insert_stores()
        except Exception as e:
            return { 'message': 'Ocurrió un error interno' }, 500

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_store()
            return { 'message': f'{name} fue borrado exitosamente' }, 200

        return { 'message': f'{name} no se encontró o ya fue borrado' }, 400
