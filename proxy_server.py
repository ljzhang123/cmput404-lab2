#!/usr/bin/env python3
import socket
import time
import sys
import multiprocessing as mp

#define address & buffer size
HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        googleIp = get_remote_ip('www.google.com')
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # receive request from client and print it
            full_data = conn.recv(BUFFER_SIZE)
            print(full_data.decode('utf-8'))
            
            # connect to google.com and send client payload
            s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s2.connect((googleIp, 80))
            s2.sendall(full_data)

            # recieve data from web server and send it back to client
            response_data = s2.recv(BUFFER_SIZE)
            s2.close()
            time.sleep(0.5)
            conn.sendall(response_data)
            conn.close()

if __name__ == "__main__":
    queue = mp.Queue()
    process = mp.Process(target=main)
    process.start()
    process.join()
