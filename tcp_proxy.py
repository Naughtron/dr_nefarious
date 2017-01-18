#!/opt/local/bin/python2.7
# TCP Proxy example


import sys
import socket
import threading

# create the server loop
def server_loop(local_host, local_port, remote_host, remote_port, recv_first):
    
    # create a socket set to deal with IPv4 and TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #bind the server
    try:
        server.bind((local_host, local_port))
        
    except:
        print "[!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!] Check for other listening sockets or correct permissions."
        sys.exit(0)
        
    print "[*] Listening on %s:%d" % (local_host, local_port)
    
    # allow five connections max
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # print out the local connection info
        print "[==>] Recv incoming connection %s:%d" % (addr[0], addr[1])
        
        
    