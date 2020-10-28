import socket
import sys
import time

try:
    x = socket.socket()
    hostName = input(str('Enter the hostname of the server'))
    port = 8080

    x.connect((hostName, port))
    print('connected to chat server')

    while 1:
        incomingMessage = s.recv(1024)
        incomingMessage = incomingMessage.decode()
        print('Server:', incomingMessage)
        message = input(str('>>'))
        message = message.encode()
        s.send(message)
        print('message has been sent...')
        if incomingMessage.lower() is 'close connection':
            x.shutdown()

    x.close()
except Exception as e:
    print('Something went wrong...')
    print('Exception from client.py', e)
