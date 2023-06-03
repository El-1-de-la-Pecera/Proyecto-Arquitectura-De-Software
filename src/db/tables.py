import sqlite3
import argparse

def create_tablas():
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            ID INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Precio REAL NOT NULL,
            Stock INTEGER NOT NULL,
            SKU INTEGER NOT NULL,
            Categoria TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            ID INTEGER PRIMARY KEY,
            Nombre TEXT NOT NULL,
            Clave REAL NOT NULL,
            Tipo INTEGER NOT NULL
        );
    ''')
    conexion.commit()
    conexion.close()