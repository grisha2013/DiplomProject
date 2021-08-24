import paramiko
import time
import socket

def send_get_command(
        ssh,
        command = '',
):
    if command == " \n": command = ' '
    if command == "exit\n":
        ssh.send(command)
        time.sleep(1)
        ssh.send("\r\n")
    else:
        ssh.send(command)
    time.sleep(1)
    part = ""
    while True:
        try:
            inpart = ssh.recv(60000).decode("utf-8")
            part += inpart
        except socket.timeout:
            break
    part = part.replace(command.replace('\n', '', 1), '', 1)
    print(part, end='')

cl = paramiko.SSHClient()
cl.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cl.connect(
    hostname="192.168.30.163",
    username="cisco",
    password="cisco",
    port=2502,
    look_for_keys=False,
    allow_agent=False
)
with cl.invoke_shell() as ssh:
    ssh.send("\r\n")
    ssh.settimeout(1)
    time.sleep(1)
    print(ssh.recv(60000).decode("utf-8"), end='')
    while True:
        command = input()
        command = command + "\n"
        send_get_command(ssh, command)
