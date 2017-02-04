# SSH revc commands

'''
this client would be used when connecting to a machine that has no ssh server (windows)
so you need to reverse things. 
send commands from your ssh server to an ssh client (n_sshclient)
'''

import threading
import paramiko
import subprocess

# ssh command method
def ssh_cmd(ip, user, password, command):
    client = paramiko.SSHClient()
    # FYI if used in the real world you would want to use ssh key auth
    '''client.load_host_keys('path to an ssh key goes here')'''
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024) # read the banner info
        while True:
            command = ssh_session.recv(1024) # gets the commnad from the ssh server
        try:
            cmd_output = subprocess.check_output(commnad, shell=True)
            ssh_session.send(cmd_output)
        except Exception, e:
            ssh_session.send(str(e))
            
        client.close()
    return
