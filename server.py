#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import os
import socketserver
import sys

try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        FILE= sys.argv[3]
except:
    sys.exit("Usage: python3 server.py IP port audio_file")

if not os.path.exists(FILE):
        sys.exit("Document doesn't exist")

TRYING = b"SIP/2.0 100 Trying\r\n"
RINGING = b"SIP/2.0 180 Ringing\r\n"
OK = b"SIP/2.0 200 OK\r\n"
BAD_REQUEST = b"SIP/2.0 400 Bad Request\r\n"
Not_Allowed = b"SIP/2.0 405 Method Not Allowed\r\n"
aEjecutar = "./mp32rtp -i 127.0.0.1 -p 23032 < " + FILE

class EchoHandler(socketserver.DatagramRequestHandler):
 
    def handle(self):
       
        message = self.rfile.read()
        line = message.decode('utf-8').split(' ')
        METHOD = line[0] 
        if len(line)<4 and len(line)>0:
                if METHOD == 'INVITE':
                   print('INVITE received')
                   self.wfile.write(TRYING + RINGING + OK + b'\r\n')
                elif METHOD == 'ACK':
                   print("ACK RECIVED")
                   os.system(aEjecutar)
                elif METHOD == 'BYE':
                   print("BYE RECIVED")
                   self.wfile.write(OK + b'\r\n')
                else:
                   self.wfile.write(Not_Allowed)
        else:
             self.wfile.write(BAD_REQUEST) 
                        
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print('Listening...')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
        
