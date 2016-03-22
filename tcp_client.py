# the following is a simple TCP client
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
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the client
client.connect((t_host, con_t_port))

# send data over connection example
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# get back a Response
resp = client.recv(4096)

# display Response to the user
print resp

'''
Description:
1. The AF_INET portion is telling the script that we are going to use a normal IPv4 address / hostname
2. The SOCK_STREAM portion is telling the script that this will be a TCP connection
3. We then make the connection using the values supplied by the user for host and port
4. We then send some data
5. We then get a response back from the host and display it to the user
'''

'''
Why would I use this?
A simple TCP Client will allow you to hit a target host to gather information. When you get a successful response
make note of what you are getting back.
EXAMPLE:

HTTP/1.1 403 Forbidden
Server: nginx/1.8.0
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
X-Powered-By: PHP/5.6.6
Cache-Control: no-cache
'''