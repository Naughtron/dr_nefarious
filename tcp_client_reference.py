import socket

tcp_address = "127.0.0.1"
tcp_port = 5005
buffer_size = 1024
message = "ALWAYSBETESTING!"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((tcp_address, tcp_port))
client_socket.send(message)
data = client_socket.recv(buffer_size)
client_socket.close()

print "data recieved: " , data