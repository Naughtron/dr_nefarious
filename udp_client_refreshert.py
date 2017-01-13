# this is a udp client refresher

import socket

target_host = "127.0.0.1"
target_port = 9999

# create the socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'''
remember that AF_INET = IPv4
remember that SOCK_STREAM = UDP
'''
# bind the client
client.bind(target_host, target_port)

# send some data
client.sendto("ALWAYSBETESTING", (target_host, target_port))

# response data
data, addr = client.recvfrom(1024)
'''
a tuple is coming back
'''

print data, addr

'''
remember there is no need to create a connect with UDP as it is connectionless
'''