import sqlite3
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

#REVISAR
def disable_product(SKU):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("UPDATE Inventario SET Estado = (SELECT ID FROM EstadoProducto WHERE Descripcion = 'Inhabilitado') WHERE SKU = ?", (SKU,))
    conn.commit()
    conn.close()

try:
    # Send data
    message = b"00050sinitserv5"
    print('sending {!r}'.format(message))
    sock.sendall(message)
    while True:
        # Look for the response
        print("Waiting for transaction-DIS")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            SKU = data.decode("utf-8")
            disable_product(SKU)
            print('Product disabled: SKU={}'.format(SKU))
            sock.sendall(b"Transaction-DIS completed")

finally:
    print ('closing socket')
    sock.close ()