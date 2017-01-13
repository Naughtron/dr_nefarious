import socket

server_tcp_ip = '127.0.0.1'
server_port = 5005
buffer_size = 20

serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_socket.bind((server_tcp_ip, server_port))
serv_socket.listen(1)

print "[*] I'm the server and listening on %s:%d " % (server_tcp_ip, server_port)

conn, addr = serv_socket.accept()

print "Connection Address: ", addr

while True:
    data = conn.recv(buffer_size)
    if not data: break
    print "revieved data: ", data
    conn.send(data) 
conn.close()