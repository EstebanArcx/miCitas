# Funcion para conectar a la base de datos
import mysql.connector
from flask import g
import os

# Configuración de la base
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME')
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
