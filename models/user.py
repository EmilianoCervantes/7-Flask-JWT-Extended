'''Poder extraer información (objetos) de la tabla user'''
from db import database

class UserModel(database.Model):
    '''TABLE AND COLUMN DEFINITIONS'''
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key = True)
    username = database.Column(database.String(80))
    password = database.Column('pass', database.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def update_and_insert_users(self):
        database.session.add(self)
        database.session.commit()

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
