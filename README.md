# Proyecto-Arquitectura-De-Software
Gestor de inventario 
con arquitectura SOA



## Servicios
Gestor de cuentas
Inventario
Ventas


## Base de datos
SQLite

## Lenguaje
Python


### nota 
* matar servicios
    * kill $(jobs -p)
+ python3 src/services/serv1.py & python3 src/services/serv2.py & python3 src/services/login.py > /dev/null & python3 main.py