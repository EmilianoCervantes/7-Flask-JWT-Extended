# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity

from models.item import ItemModel


class ItemList(Resource):
    @jwt_optional
    def get(self):
        # get_jwt_identity -> Lo que guardamos en el access_token como identity
        user_id = get_jwt_identity()
        return { 'items': [item.json() for item in ItemModel.find_all()] }


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', required=True, type=float, help='Este campo no puede estar vacío')
    parser.add_argument('store_id', required=True, type=int, help='Cada item debe ligarse a una tienda')

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return { 'message': None }, 404

    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return { 'message': f'Ya existe {name}' }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.update_and_insert_items()
        except Exception as e:
            return { 'message': 'Ocurrió un error interno' }, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        '''
            Uso de jwt claims.
            Que no puedas borrar si no eres admin.
        '''
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return { 'message': 'Debes ser admin' }, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return { 'message': f'{name} fue borrado exitosamente' }, 200
        return { 'message': f'{name} no se encontró o ya fue borrado' }, 400

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.update_and_insert_items()

        return item.json(), 201
