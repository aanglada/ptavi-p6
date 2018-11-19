#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.

try:
	METHOD = sys.argv[1]
	LOGIN = sys.argv[2].split('@')[0]
	IP = sys.argv[2].split('@')[1].split(':')[0]
	PORT = int(sys.argv[2].split(':')[1])

except (IndexError, ValueError):
	sys.exit('Usage: python3 client.py method receiver@IP.SIPport')


# Contenido que vamos a enviar

LINE = METHOD + ' sip:' + LOGIN + '@' + IP + ':' + str(PORT) + 'SIP/2.0\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP, PORT))

    print("Enviando: " + LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

    line = data.decode('utf-8').split('\r\n')
    if line[0].split()[-1] == 'Trying' and METHOD == 'INVITE':
        print(line[0] + '\n' + line[1] + '\n' + line[2])
        my_socket.send(bytes(LINE.replace('INVITE', 'ACK'), 'utf-8') + b'\r\n')
    else:
        print(line[0])

print("Fin.")
