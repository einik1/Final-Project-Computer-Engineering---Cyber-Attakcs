#!/usr/bin/python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('10.0.2.15', 4444))
finish = True

while finish:
    client_data = raw_input("what do you send?\n")
    if client_data != '':
        if client_data.lower() == "bye":
            client_socket.send("bye")
            break
	elif client_data.lower() == "floodattack":
            for sport in range(1, 1000):
                client_socket.send(str(sport)+"\n")
        else:
            client_socket.send(client_data)
            data = client_socket.recv(2048)
            print "the server sent: " + data + "\n"
client_socket.close()
