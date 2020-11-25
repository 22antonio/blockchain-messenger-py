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
        # recieving messagem, decoding message, check if wants to closed
        # displays message
        incomingMessage = x.recv(1024)
        incomingMessage = incomingMessage.decode()
        if 'close connection' in incomingMessage.lower():
            print('connection is being closed')
            x.close()
            break
        print('Server:', incomingMessage)

        # asks for input to send a message, encodes message
        # sends message
        message = input(str('>>'))
        message = message.encode()
        x.send(message)
        print('message has been sent...')

        # decodes message to see if client wants to end connection
        message = message.decode()
        if 'close connection' in message.lower():
            print('connection is being closed')
            x.close()
            break
except Exception as e:
    print('Something went wrong...')
    print('Exception type', type(e))
    print('Exception from client.py', e)
