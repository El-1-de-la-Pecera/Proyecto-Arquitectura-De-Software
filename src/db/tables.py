import sqlite3
import argparse

def create_tablas():
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Precio REAL NOT NULL,
            Stock INTEGER NOT NULL,
            SKU INTEGER NOT NULL,
            Categoria TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EstadoProducto (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Descripcion TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Clave REAL NOT NULL,
            Rol INTEGER NOT NULL
        );
    ''')
    conexion.commit()
    conexion.close()

def remove_tablas():
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute('''
        DROP TABLE IF EXISTS inventario;
    ''')
    cursor.execute('''
        DROP TABLE IF EXISTS usuarios;
    ''')
    conexion.commit()
    conexion.close()

def insertar_usuario(nombre, clave, tipo):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO usuarios (Nombre, Clave, Tipo) VALUES (?, ?, ?);
    ''', (nombre, clave, tipo))
    conexion.commit()
    conexion.close()
