'''
Contendrá todo lo de SQLAlchemy
'''
from flask_sqlalchemy import SQLAlchemy

'''
Este objeto recorrerá todos los objetos que le digamos,
y linkeará/mapeará esos objetos a filas/rows en nuestra base de datos.
'''
database = SQLAlchemy()
