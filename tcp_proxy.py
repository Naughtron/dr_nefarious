#!/opt/local/bin/python2.7
# TCP Proxy example

"""
example use / quick test: 
on a linux box run the following: 
python tcp_proxy.py 127.0.0.1 21 ftp.target.ca 21 True

in a new terminal run: 
ftp 127.0.0.1

you will then see data recv'ed
[*] Listening on 127.0.0.1:21
[==>] Recv incoming connection 127.0.0.1:39560
"""

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
        
        
    # create a new thread to so you can talk to the remote 
    # connection requests that coem in are handed over to proxy_handler 
    proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, recv_first))


    # start the thread
    proxy_thread.start()

    # proxy_handler 
    def proxy_handler(client_socket, remote_host, remote_port, recv_first):
        # create connection socket
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect over the socket 
        remote_socket.connect((remote_host, remote_port))

        #recv data from the remote end if set
        if recv_first:

            remote_buffer = recv_from(remote_socket)
            hexdump(remote_buffer) # wat? clear this up so you understand 

            # send data to the response handler
            remote_buffer = response_handler(remote_buffer)

        # if there is data to send to the local machine
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost " % len(remote_buffer)
            client_socket.send(remote_buffer)

        # now loop and rad from local
        # send to remote / send to local
        while True: 

            # read from the local
            local_buffer = recv_from(client_socket)

            if len(local_buffer):
                print "[==>] Recv'd %d bytes from localhost " % len(local_buffer)
                hexdump(local_buffer) # again wat? Clear this up so you understand

                # send data to request handler
                local_buffer = request_handler(local_buffer)

                # send off the data to the remote host
                remote_socket.send(local_buffer)
                print "[==>] Data sent to the remote"

                # recv back a resposne
                remote_buffer = recv_from(remote_socket)

                if len(remote_buffer):

                    print "[<==] Recv'd %d bytes from remote. " % len(remote_buffer)
                    hexdump(remote_buffer)

                    # send response handler over local socket
                    client_socket.send(remote_buffer)
                    print "[<==] Sent to localhost."

                # if there is no more data to transmit close the connections 
                if not len(local_buffer) or not len(remote_buffer):
                    client_socket.close()
                    remote_socket.close()
                    print "[*] There is no more data to transmit. Closing Connections."

                    # break out
                    break

def hexdump(src, length=16):
    result = [] # empty dict 
    digits = 4 if isinstance(src, unicode) else 2
    
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    print b'\n'.join(result)
    
def receive_from(connection):

    buffer = ""

    # We set a 2 second time out depending on your 
    # target this may need to be adjusted
    connection.settimeout(2)

    try:
            # keep reading into the buffer until there's no more data
        # or we time out
            while True:
                data = connection.recv(4096)
                if not data:
                    break
                buffer += data
    except:
        pass

        return buffer

# modify any requests destined for the remote host
def request_handler(buffer):
    # perform packet modifications
    return buffer

# modify any responses destined for the local host
def response_handler(buffer):
    # perform packet modifications
    return buffer
    
def main():

        # show usage example
        # this is a way to make sure the correct number of args is coming in 
        if len(sys.argv[1:]) != 5:
            print "Usage: ./tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [recv_first]"
            print "Ex: ./tcp_proxy.py 127.0.0.1 9000 10.12.13.1 9000 True"
            sys.exit(0)

        # setup the local listener
        local_host = sys.argv[1]
        local_port = int(sys.argv[2])

        # setup remote target connection
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])

        # config so you collect data prior to sending 
        recv_first = sys.argv[5]

        # apply the setting
        if "True" in recv_first:
            recv_first = True
        else:
            recv_first = False

        # now create a listening socket
        # call server_loop with the following: 
        server_loop(local_host, local_port, remote_host, remote_port, recv_first)

main()
