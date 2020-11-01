import socket
import sys
import time

try:
    x = socket.socket()

    hostName = socket.gethostname()
    print('server will start host: ', hostName)

    port = 8080

    x.bind((hostName, port))
    print('server done binding to host and port successfully')
    print('server is waiting for incoming connections')

    x.listen(1)

    connection,address = x.accept()
    print(address, 'has connected to the server and is now online...')

    while 1:
        displayMessage = input(str('>>'))
        displayMessage = displayMessage.encode()
        connection.send(displayMessage)
        print('message has been sent...')

        displayMessage = displayMessage.decode()
        if 'close connection' in displayMessage.lower():
            print('connection is being closed')
            x.close()
            break
        
        incomingMessage = connection.recv(1024)
        incomingMessage = incomingMessage.decode()
        print('Client:', incomingMessage)
        if 'close connection' in incomingMessage.lower():
            print('connection is being closed')
            x.close()
            break
except Exception as e:
    print('Something went wrong')
    print('Exception type', type(e))
    print('Exception from server.py', e)
