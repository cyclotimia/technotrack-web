#!/usr/local/bin/python

# implement serving multiple users by forking, as opposed to simple.py

import os
import socket
import sys

server_socket = socket.socket() # выдел память под сокет
server_socket.bind(('', 8080)) # '' is an ip address; by '' we listen to all ip addresses
server_socket.listen(10) # 10 is queue size

while True: # родительскому процессу из цикла выходить не нужно, он слушает постоянно
    client_socket, remote_address = server_socket.accept() 
    # читай мануал - https://docs.python.org/2/library/socket.html#socket-objects
    # ^^ возвращает выделенный ОСью дескриптор процесса (handle) = это client_socket, и ip адрес с которого к нам пришли
    # при этом текущ процесс переходит в сост-е sleep пока не приконнектится следующий
    child_pid = os.fork() # return 0 or child_pid
    # ^^ как только кто-то приконнектится - после принятия каждого нового соед-я форкаемся
    # форк = создать дочерний процесс-копию текущего процесса со всей его памятью, стеком, дескрипторами и тд
    if child_pid == 0: # значит находимся во вновь созданном, дочернем процессе
    # работа дочернего процесса:
        request = client_socket.recv(1024)
        client_socket.send(request.upper())
        print '(child {}) {} : {}'.format(child_pid, client_socket.getpeername(), request)
        client_socket.close()
        sys.exit() 
        # отработали и завершили дочерний процесс
    else: # если не 0, то продолжается вып-е родительского процесса
        client_socket.close()

server_socket.close()
