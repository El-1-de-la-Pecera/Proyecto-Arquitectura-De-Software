import sqlite3
import sys
import socket
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)


def create_user(Nombre, Clave, Rol):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (Nombre, Clave, Rol) VALUES (?, ?, ?)", (Nombre, Clave, Rol))
    conn.commit()
    conn.close()

try:
    # Send data
    message = b"00050sinitserv6"
    print ('sending {!r}'.format (message))
    sock.sendall(message)
    while True:
        # Look for the response
        print ("Waiting for transaction - New_USER")
        amount_received = 0
        amount_expected = int(sock.recv (5))
        while amount_received < amount_expected:
            data = sock.recv(amount_received - amount_expected)
            amount_received+=len(data)
            Nombre = data[0]
            Clave = data[1]
            Rol = data[2]
            create_user(Nombre, Clave, Rol)
            print ('received {!r}'.format (data))

finally:
    print ('closing socket')
    sock.close()