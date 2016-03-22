# the following is a simple TCP server. Please note this can be used to test the tcp_client as well
# Author: Naughtron
# import:
# python socket lib
import socket
# python threading lib
import threading

# bind the IP address for the server
b_ip = "0.0.0.0"
# set the listening port for the server
b_port = 9999

# initial server setup
n_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# remember AF_INET = IPv4, and SOCK_STREAM = TCP

# bind the server
n_server.bind((b_ip, b_port))

# set connection limit of the server
n_server.listen(5)

# show the user the details of the setup
print "[*] Listening on %s:%d" % (b_ip, b_port)

# handle any tcp client connecting to the server
def handle_client(client_socket):
    # show the user what the client is sending
    n_request = client_socket.recv(1024)
    print "[*] Recieved: %s" % n_request

    # send a packet back to the connecting client
    client_socket.send("IMAWIZARD")
    # close the connection
    client_socket.close()

# start the server loop:
while True:
    client, addr = n_server.accept()
    print "[*] Accecpted connection from: %s:%d" % (addr[0], addr[1])

    #handle the incoming data
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
