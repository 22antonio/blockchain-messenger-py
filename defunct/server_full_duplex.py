import socket
import select

#set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# address 'already in use' error
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind and listen
server_socket.bind((socket.gethostname(), 1234))
server_socket.listen()

# list of sockets and clients dict. this will help keep track of all the clients that will make a connection
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {socket.gethostname()}:{1234}...')

# Handles message receiving
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(100)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except Exception as e:
        # something went wrong
        print(type(e))
        print('err from receive_message', e)
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:

        # if new conncetion, accept it
        if notified_socket == server_socket:

            # accpet new connection
            client_socket, client_address = server_socket.accept()

            # receive client name
            user = receive_message(client_socket)

            # if false - client disconnected before sent name
            if user is False:
                continue

            # added socket to list
            sockets_list.append(client_socket)

            # save username and header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
        # else existing socket is sending a message
        else:
            # receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, clean up
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # remove from list for sockekt.socket()
                sockets_list.remove(notified_socket)

                # remove from out list of users
                del clients[notified_socket]

                continue

            # who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # iterate over connected clients and broadcast message
            for client_socket in clients:

                # don't send it to sender
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

        # handle socket expetions
        for notified_socket in exception_sockets:
            # remove from list
            sockets_list.remove(notified_socket)

            # remove from list of users
            del clients[notified_socket]
