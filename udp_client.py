# the following is a simple UDP client
# Author: Naughtron
# import:
# python socket lib
import socket

# ask user for host address
t_host = raw_input("Enter Host You Want To Connect To: ")
# ask user for port
t_port = raw_input("Enter Port You Want To Use: ")
con_t_port = int(t_port)

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# connect to the client
client.connect((t_host, con_t_port))

# send data over connection example
client.sendto("ALWAYSBETESTING", (t_host, con_t_port))

# recieve the data you sent
data, addr = client.recvfrom(4096)

# display Response to the user
print data

'''
Description:
1. The AF_INET portion is telling the script that we are going to use a normal IPv4 address / hostname
2. The SOCK_DGRAM portion is telling the script that this will be a UDP connection
3. We then make the connection using the values supplied by the user for host and port
4. We then send some data
5. We then get a response back from the host and display it to the user
'''

'''
Why would I use this?
A simple UDP Client will allow you to hit a target host to gather information. When you get a successful response
make note of what you are getting back. Please note there is no connect in this script as UDP is a connectionless
protocol
'''