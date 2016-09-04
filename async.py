#!/usr/local/bin/python
# асинхронная схема для нагруженных систем

import socket
import select

server_socket = socket.socket()
server_socket.bind(('', 8080))
server_socket.setblocking(0) # не блокирующий (не как socket.accept() )
# socket.setblocking(flag)
# Set blocking or non-blocking mode of the socket: 
# if flag is 0, the socket is set to non-blocking, else to blocking mode. 
# Initially all sockets are in blocking mode. 
# - In non-blocking mode, if a recv() call doesn’t find any data, 
# or if a send() call can’t immediately dispose of the data, an error exception is raised; 
# - in blocking mode, the calls block until they can proceed. 
# s.setblocking(0) is equivalent to s.settimeout(0.0); s.setblocking(1) is equivalent to s.settimeout(None).
server_socket.listen(10)

inputs = {server_socket} # сокеты из которых читаем
outputs = {} # сокеты в которые пишем
excepts = [] # ошибки

while 1:
    input_ready, output_ready, except_ready = select.select(list(inputs), outputs.keys(), excepts, 0.5)
    # https://docs.python.org/3/library/select.html#select.select
    for s in input_ready:
        if s == server_socket:
            client_socket, remote_address = server_socket.accept()
            client_socket.setblocking(0)
            inputs.add(client_socket)
        else:
            request = s.recv(1024)
            print '{} : {}'.format(s.getpeername(), request)
            outputs[s] = request.upper()
            inputs.remove(s)
    for s in output_ready:
        if s in outputs:
            s.send(outputs[s])
            del outputs[s]
            s.close()
