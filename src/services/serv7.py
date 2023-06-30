import sqlite3
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

#REVISAR
def update_user(Nombre, Clave, Rol):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE usuarios SET Nombre=?, Clave=?, Rol=? WHERE ID=?", (Nombre, Clave, Rol))
    conn.commit()
    conn.close()

try:
    # Send data
    message = b"00050sinitserv7"
    print('sending {!r}'.format(message))
    sock.sendall(message)
    while True:
        # Look for the response
        print("Waiting for transaction-UPD_USER")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            data = data.decode("utf-8").split(",")
            #ID = int(data[0])
            #Nombre = data[1]
            #Clave = float(data[2])
            #Rol = int(data[3])
            #SKU = data[4]
            #Categoria = data[5]
            
            Nombre = data[0]
            Clave = float(data[1])
            Rol = data[2]
            update_user(Nombre, Clave, Rol)
            print('Product updated: Nombre={}, Clave={}, Rol={}'.format(Nombre, Clave, Rol))
            sock.sendall(b"Transaction-UPD_USER completed")

finally:
    print ('closing socket')
    sock.close ()