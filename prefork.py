#!/usr/local/bin/python
# https://docs.python.org/2/library/socket.html#socket-objects

import os
import socket
import sys


server_socket = socket.socket()
server_socket.bind(('', 8080))
server_socket.listen(10)

for i in range(4):
    child_pid = os.fork()
    # сначала форкаем 4 процесса и каждый из них пытается читать из созданного нами серверного сокета
    if child_pid == 0:
        try:
            while True:
                client_socket, remote_address = server_socket.accept()
                request = client_socket.recv(1024)
                client_socket.send(request.upper())
                print '(child {}) {} : {}'.format(os.getpid(), client_socket.getpeername(), request)
                client_socket.close()
        except KeyboardInterrupt:
            sys.exit()

try:
    os.waitpid(-1, 0)
except KeyboardInterrupt:
    sys.exit()

# недостаток: в какой-то момент не хватит ресурсов
# lдост-во: даже если придут 2000 чел, все равно будет только 4 процесса
