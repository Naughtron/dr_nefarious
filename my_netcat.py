# my very own netcat

import sys
import socket
import getopt
import threading
import subprocess

# def all the global vars
listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

# usage info 
def usage():
    print "***!N Net Tools***"
    print
    print "Usage: my_netcat.py -t target_host -p port"
    print
    print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute a given file upon recv connection"
    print "-c --command             - init a command shell"
    print "-u --upload=destination  - upon recv connection upload file and write to [destination]"
    print
    print "Examples:"
    print "my_netcat.py -t 64.30.228.82 -p 5555 -l -c"
    print "my_netcat.py -t 64.30.228.82 -p 5555 -l -u=C:\\badthing.exe"
    print "my_netcat.py -t 64.30.228.82 -p 5555 -l -e\"cat /etc/passwrd\""
    print "echo 'ALWAYS BE TESTING!' | ./my_netcat.py -t 64.30.228.82 -p 131"
    sys.exit(0)
    
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try: 
        # connect to the target
        client.connect((target, port))
        
        # this checks to see if anything came in from stdin
        # if that is cool then it is shipped off to the target
        if len(buffer):
            client.send(buffer)
    
            while True:
                # wait for the data to come back 
                recv_len = 1
                response = ""
                
                while recv_len:
                    data = client.recv(4096)
                    recv_len = len(data)
                    response += data
                    
                    if recv_len < 4096:
                        break
                print response
                
                # wait for more input
                buffer = raw_input("")
                buffer += "\n"
                
                # send it off
                client.send(buffer)
    
    except:
        print "[*] Exception Exiting"
        # kill the connection 
        client.close()
            
def server_loop():
    global target
    
    # if no target is defined by the user then listen on all interfaces
    if not len(target):
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to what the user has entered 
    server.bind((target, port))
    # setting listen to 1 connection for now
    server.listen(5)
    
    while True: 
        client_socket, addr = server.accept()
        # create new thread for the client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()
        
def run_command():
    # trim
    command = command.rstrip()
    
    # run the command and get the output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to run your command. \r\n"
        
    # send the output back to the user
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    
    # check for upload
    if len(upload_destination):
        
        # read bytes and write to destination
        file_buffer = ""
        
        # keep reading until there is nothing remaining
        while True: 
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
                
        # take all bytes and write them out
        try:
            file_description = open(upload_destination, "wb")
            file_description.write(file_buffer)
            file_description.close()
            
        except:
            client_socket.send("Failed to save file to %s\%r\%n" % upload_destination)
            
    # check for a command
    if len(execute):
        # run the command
        output = run_command(execute)
        
        client_socket.send(output)
        
    # loop for command shell
    if command:
        while True:
            # show prompt
            client_socket.send("<!N> ")
            
            # recv until user hits enter
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            # send back the command output to the user
            response = run_command(cmd_buffer)
            
            # send back the response
            client_socket.send()
    
# main
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    # read command line options 
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", 
                                                                 "listen", 
                                                                 "execute", 
                                                                 "target", 
                                                                 "port", 
                                                                 "command", 
                                                                 "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    
    for a, o in opts:
        if o in ("-h", "--help"):
            useage()
        elif o in ("-l", "--listen"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
            
    # listen or send data?
    if not listen and len(target) and port > 0:
        # read the buffer from command line 
        # NOTE: you need to send CRTL-D if not sending input
        buffer = sys.stdin.read()
        # send data
        client_sender(buffer)
    
    if listen: 
        # listen here, and wait to see if the user wants to 
        # upload, execute, drop files, depending on above.
        server_loop()
        
if __name__ == '__main__':
    main()