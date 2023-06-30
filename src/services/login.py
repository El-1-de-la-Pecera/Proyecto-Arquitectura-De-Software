import socket
import sqlite3
from utils import bus_format
import paramiko
import json
def login(nombre, clave):
    con = sqlite3.connect("db.sqlite3")
    cursor = con.cursor()
    query = f"""SELECT * FROM usuarios WHERE Nombre = '{nombre}' AND Clave = '{clave}' ;"""
    cursor.execute(query)
    rows = cursor.fetchall()
    con.commit()
    con.close()
    if (len(rows) == 0):
        return None
    else:
        return rows[0]


with open('config.json') as file:
    config = json.load(file)

server_ip = config['server_ip']
server_port = config['server_port']
username = config['username']
password = config['password']

bus_server_ip = config['bus_server_ip']
bus_server_port = config['bus_server_port']


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server_ip, port=server_port, username=username, password=password)
sock = client.invoke_shell()

bus_socket = client.get_transport().open_session()
bus_socket.exec_command(f"nc {bus_server_ip} {bus_server_port}")
bus_socket.send(b"00050sinitserv0")


# message = b"00050sinitserv0"
# sock.sendall(message)
#status = sock.recv(4096)[10:12].decode('UTF-8')
status = bus_socket.recv(4096)[:].decode('UTF-8')


print(status)
# if status == 'OK':
#     print('Servicio login iniciado de forma correcta\n')
#     while True:
#         received_message = sock.recv(4096).decode('UTF-8')
#         print(received_message)
#         client_id = received_message[5:10]
#         data = json.loads(received_message[10:])
#         ans = login(data['Nombre'], data['Clave'])
#         response = bus_format(ans, str(client_id)).encode('UTF-8')
#         sock.send(response)
