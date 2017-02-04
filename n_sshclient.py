# SSH Client
# this is using paramiko with pycrypto

import threading
import paramiko
import subprocess

# ssh command method
def ssh_cmd(ip, user, password, command):
    client = paramiko.SSHClient()
    # FYI if used in the real world you would want to use ssh key auth
    """client.load_host_keys('path to an ssh key goes here')"""
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=password)
    ssh_session = client.get_transport().open_session()
    
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return