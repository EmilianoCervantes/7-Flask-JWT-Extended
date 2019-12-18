'''
Propósito: crear todas las tablas que se necesitan para este API.
'''
import sqlite3

connection = sqlite3.connect('section4.db')
cursor = connection.cursor()

# Verificar si la tabla existe o no.
# PODER correr este script múltiples veces a diferencia de test,
# donde había que borrar data.db a cada rato.

# id INTEGER PRIMARY KEY terminología de sqlite3
# INTEGER en vez de int es para que sea un int autoincremental
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)

connection.commit()
connection.close()
