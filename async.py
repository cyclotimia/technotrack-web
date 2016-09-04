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
    # с таймаутом 0,5 вернет нам 3 списка: сокеты из которых надо читать, сокеты в которые можно писать сейчас, сокеты в к-х произошла ошибка
    # и мы просто итерируемся по трем этим спискам
    for s in input_ready:
        if s == server_socket: # если пришел новый
            client_socket, remote_address = server_socket.accept()
            client_socket.setblocking(0)
            inputs.add(client_socket) # добавляем клиента в список сокетов из которых читаем
        else:
            request = s.recv(1024) # если уже есть в списке
            # socket.recv(bufsize[, flags])
# Receive data from the socket. The return value is a bytes object representing the data received. 
# The maximum amount of data to be received at once is specified by bufsize.
            print '{} : {}'.format(s.getpeername(), request)
            outputs[s] = request.upper() # переводим полученный ответ в апперкейс и закидываем в список outputs под индексом s
            inputs.remove(s) # удаляем s из списка на вывод
    for s in output_ready:
        if s in outputs:
            s.send(outputs[s]) # шлем
            del outputs[s] # удаляем
            s.close()
