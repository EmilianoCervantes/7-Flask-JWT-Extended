'''
Modelo de la tienda.
Ligar el id de las tiendas a un store_id en cada item.
'''
from db import database

class StoreModel(database.Model):
    '''TABLE AND COLUMN DEFINITIONS'''
    __tablename__ = 'stores'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    items = database.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return { 'name': self.name, 'items': [item.json() for item in self.items.all()] }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # POST y PUT al mismo tiempo
    def update_and_insert_stores(self):
        database.session.add(self)
        database.session.commit()

    def delete_store(self):
        database.session.delete(self)
        database.session.commit()
