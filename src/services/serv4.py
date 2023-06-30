import sqlite3
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

#REVISAR
#def update_product(ID, Nombre, Precio, Stock, SKU, Categoria):
def update_product(Nombre, Precio, Stock, SKU, Categoria):    
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    #c.execute("UPDATE inventario SET Nombre=?, Precio=?, Stock=?, SKU=?, Categoria=? WHERE ID=?", (Nombre, Precio, Stock, SKU, Categoria, ID))
    c.execute("UPDATE inventario SET Nombre=?, Precio=?, Stock=?, SKU=?, Categoria=? WHERE ID=?", (Nombre, Precio, Stock, SKU, Categoria))
    conn.commit()
    conn.close()

try:
    # Send data
    message = b"00050sinitserv4"
    print('sending {!r}'.format(message))
    sock.sendall(message)
    while True:
        # Look for the response
        print("Waiting for transaction-UPD")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            data = data.decode("utf-8").split(",")
#            ID = int(data[0]) ---- Arreglar los indices de data
            Nombre = data[1]
            Precio = float(data[2])##ES FLOAT? -> DEFINIDO POR REAL##
            Stock = int(data[3])
            SKU = int(data[4])
            Categoria = data[5]
#            update_product(ID, Nombre, Precio, Stock, SKU, Categoria)
            update_product(Nombre, Precio, Stock, SKU, Categoria)
#            print('Product updated: ID={}, Nombre={}, Precio={}, Stock={}, SKU={}, Categoria={}'.format(ID, Nombre, Precio, Stock, SKU, Categoria))
            print('Product updated: Nombre={}, Precio={}, Stock={}, SKU={}, Categoria={}'.format(Nombre, Precio, Stock, SKU, Categoria))
            sock.sendall(b"Transaction-UPD completed")

finally:
    print ('closing socket')
    sock.close ()