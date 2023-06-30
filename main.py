import argparse
import socket as sk
import time
from src.services.utils import bus_format
from src.db.tables import create_tablas, remove_tablas, insertar_usuario
import paramiko
import json

with open('config.json') as file:
    config = json.load(file)

server_ip = config['server_ip']
server_port = config['server_port']
username = config['username']
password = config['password']


class App:
    def __init__(self, login_service, services=[]) -> None:        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server_ip, port=server_port, username=username, password=password)
        self.sock = client.invoke_shell()
        self.login_service = login_service
        self.services = services
        transport = client.get_transport()
        
        if transport and transport.is_active():
            print("Conexión SSH establecida correctamente.")
        else:
            print("No se pudo establecer la conexión SSH.")

    def send_msg(self, msg, service_id):
        req = bus_format(msg, service_id).encode('utf-8')
        self.sock.sendall(req)
        res = self.sock.recv(1024).decode('utf-8')
        return res


    def login(self):
        inputs = {}
        for i in range(len(self.login_service['inputs'])):
            actual_input = self.login_service['inputs'][i]
            key = actual_input['key']
            inputs[key] = input(actual_input['desc'])
        req = bus_format(inputs, self.login_service['id']).encode('utf-8')
        self.sock.sendall(req)
        res = self.send_msg(inputs, self.login_service['id'])
        return res

    def login_menu(self):
        while True:
            print("Bienvenido \n")
            print("Menu de opciones:\n")
            print("Opcion 0: Salir \n")
            print("Opcion 1: {}".format(self.login_service['desc']))
            option = input('Ingrese una opcion: ')
            if option == '1':
                res = self.login()
                data = eval(res[12:])
                if res[10:12] == 'NK':
                    print('Servicio no disponible')
                    pass
                elif data == None:
                    print('Login fallido')
                    pass
                else:
                    print('Login exitoso')
                    break
            elif option == '0':
                return
            else:
                print("Opcion no valida")
        self.menu(0)

    def menu(self, type_id):
        while True:
            input("Presione enter para continuar")
            print("Bienvenido \n")
            print("Menu de opciones:\n")
            print("Opcion 0: Salir \n")
            available_services = [
                service for service in self.services if type_id in service['user_types']
            ]
            services = {}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion {}: {}".format(i+1, actual_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '0':
                return
            elif option in services:
                service = services[option]
                inputs = {}
                for i in range(len(service['inputs'])):
                    actual_input = service['inputs'][i]
                    key = actual_input['key']
                    inputs[key] = input(actual_input['desc'])                
                res = self.send_msg(inputs, service['id'])
                print(res)
                if res[10:12] == 'NK':
                    print('Servicio no disponible')
                    pass
                else:
                    service['function'](res)
            else:
                print("Opcion no valida")


if __name__ == '__main__':
    app = App(
        login_service={
            'id': 'serv0',
            'desc': 'Iniciar sesión',
            'inputs': [
                {
                    'key': 'Nombre',
                    'desc': 'Ingresa tu nombre: '
                },
                {
                    'key': 'Clave',
                    'desc': 'Ingresa tu clave: '
                }
            ]
        },
        services=[
            {
                'id': 'serv1',
                'desc': 'Crear producto',
                # tipos de usuarios: 0: admin, 1: vendedor
                'user_types': [0],
                'function': 'serv1',
                'inputs': [
                    {
                        'key': 'Nombre',
                        'desc': 'Ingresa el nombre del producto: ',
                    },
                    {
                        'key': 'precio',
                        'desc': 'Ingresa el precio del producto: ',
                    },
                    {
                        'key': 'stock',
                        'desc': 'Ingresa el stock: '
                    },
                    {
                        'key': 'SKU',
                        'desc': 'Ingresa el código SKU: '
                    },
                    {
                        'key': 'categoria',
                        'desc': 'Ingresa la categoría del producto: '
                    }
                ]
            },
            {
                'id': 'serv2',
                'desc': 'Buscar producto',
                'user_types': [0, 1],
                #'function': buscar_producto,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del producto: '
                    }
                ]
            },
            {
                'id': 'serv3',
                'desc': 'Eliminar producto',
                'user_types': [0],
                #'function': eliminar_producto,
               'inputs': [
                    {
                        'key': 'ID',
                        'desc': 'Ingresa el id del producto: ',
                    }
                ]
            }
        ]
    )

#    remove_tablas()
#    create_tablas()
#    insertar_usuario('admin', 'admin', 0)
    app.login_menu()
