# this is a TCP client referesher 

import socket

target_host = "127.0.0.1"
target_port = 9999

# create a new socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
'''
remember that AF_INET = IPv4
remember that SOCK_STREAM = TCP
'''

# connect the client
client.connect((target_host, target_port))

# send data using the client
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# get back the response
response = client.recv(4096) # <-- this is as much data as I want back 
print response

'''
This script assumes that the connection is going to work. 

This script assumes that the server is waiting for us to connect, 
and not the other way where the server contacts us and waits for a response. 


'''

