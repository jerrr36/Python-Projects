#!/usr/bin/env python3

import socket

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 5555       # Port to listen on (non-privileged ports are > 1023)

def cxn():
    
    
    with conn:
        print('Connected by', addr)
        conn.settimeout(3)
        while True:
          
            try:
                data = conn.recv(1024)
                
                if not data:
                    #print(data)
                    continue
                print(data)
            except:
                break


while True:
    print("Looking for connections")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.settimeout(3)
        try:
            s.listen()
            conn, addr = s.accept()
            cxn()
        except:
            continue
    
    
    
                
            