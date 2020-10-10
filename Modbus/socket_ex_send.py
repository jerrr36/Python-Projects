#!/usr/bin/env python3

import socket
#accept from all ips
HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 5555       # Port to listen on (non-privileged ports are > 1023)


#connection function
def cxn():
    
    
    with conn:
        print('Connected by', addr)
        conn.settimeout(3)
        Toggle = True
        
        #While loop disconnects when lost connection
        while True:
            
            data = conn.recv(1024)
            #if nothing was received, don't send anything and go back to beginning of loop
            if  not data:
                continue
            if Toggle == True:
                Toggle = not Toggle
                conn.send(b'0')
                
                
            else:
                conn.send(b'1')
                Toggle = not Toggle
                
                
            #print(data)
            #print(toggle)
            
            

##main loop, waits for connection, then uses cxn func
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
    
    
    
                
            