import socket
import sys
import time

try:
    x = socket.socket()
    hostName = input(str('Enter the hostname of the server: '))
    port = 8080

    x.connect((hostName, port))
    print('connected to chat server')

    while 1:
        incomingMessage = x.recv(1024)
        incomingMessage = incomingMessage.decode()
        if 'close connection' in incomingMessage.lower():
            print('connection is being closed')
            x.close()
            break
        print('Server:', incomingMessage)

        message = input(str('>>'))
        message = message.encode()
        x.send(message)
        print('message has been sent...')
        
        message = message.decode()
        if 'close connection' in message.lower():
            print('connection is being closed')
            x.close()
            break
except Exception as e:
    print('Something went wrong...')
    print('Exception type', type(e))
    print('Exception from client.py', e)
