'''
Representación interna de cómo se ve y qué hace un item
'''
from db import database

class ItemModel(database.Model):
    '''TABLE AND COLUMN DEFINITIONS'''
    __tablename__ = 'items'
    # Decirle a SQLAlchemy qué columnas contiene
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(80))
    price = database.Column(database.Float(precision=2))

    store_id = database.Column(database.Integer, database.ForeignKey('stores.id'))
    store = database.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store': self.store_id
        }
    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    # POST y PUT al mismo tiempo
    def update_and_insert_items(self):
        # Útil tanto para UPDATE como INSERT
        database.session.add(self)
        database.session.commit()

    def delete_item(self):
        database.session.delete(self)
        database.session.commit()
