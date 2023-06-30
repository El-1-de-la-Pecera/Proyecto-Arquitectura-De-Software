import sqlite3
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)

sock.connect(server_address)

message = b"00050sinitserv9"

def search_user(Nombre):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT FROM usuarios WHERE Nombre=?", (Nombre,))
    conn.commit()
    conn.close()
    return c.fetchall()
