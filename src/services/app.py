import socket

# Configuración del servidor
host = 'localhost'
port = 8080

# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)
print(f"Servidor escuchando en {host}:{port}")

# Aceptar conexiones entrantes
client_socket, client_address = server_socket.accept()
print(f"Cliente conectado desde {client_address[0]}:{client_address[1]}")

# Recibir y procesar mensajes del cliente
while True:
    data = client_socket.recv(1024).decode('utf-8')
    if not data:
        break
    print(f"Mensaje recibido: {data}")
    
    # Procesar el mensaje y enviar una respuesta
    response = f"Respuesta a '{data}'"
    client_socket.sendall(response.encode('utf-8'))

# Cerrar las conexiones
client_socket.close()
server_socket.close()
