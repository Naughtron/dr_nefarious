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
        
        
    # create a new thread to so you can talk to the remote 
    # connection requests that coem in are handed over to proxy_handler 
    proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, recv_first))


    # start the thread
    proxy_thread.start()

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
        server_loop(local_host, local_port, remote_host, remote_port, recv_first)

main()
