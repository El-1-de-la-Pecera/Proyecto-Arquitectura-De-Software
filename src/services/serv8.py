import sqlite3
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)

def delete_user(Nombre):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE Nombre=?", (Nombre,))
    conn.commit()
    conn.close()

try:
    # Send data
    message = b"00050sinitserv8"
    print ('sending {!r}'.format (message))
    sock.sendall(message)
    while True:
        # Look for the response
        print ("Waiting for transaction-DEL USER")
        amount_received = 0
        amount_expected = int(sock.recv (5))
        while amount_received < amount_expected:
            data = sock.recv (amount_expected - amount_received)
            amount_received += len (data)
            print(data.decode("utf-8"))
            delete_user(data.decode("utf-8"))
            print ("Transaction-DEL USER completed")
            sock.sendall(b"Transaction-DEL USER completed")
            
finally:
    print ('closing socket')
    sock.close ()