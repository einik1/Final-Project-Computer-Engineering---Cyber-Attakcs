import socket
import select
import time
import random
from datetime import datetime

def send_waiting_messages(wlist1, messages_to_send1):
    for message in messages_to_send1:
        (client_socket, data) = message
        if client_socket in wlist1:
                client_socket.send(data)
                messages_to_send1.remove(message)



server_socket = socket.socket()
#TODO put your IP
server_socket.bind(("10.0.2.15", 4444))
server_socket.listen(5)
open_client_sockets = []
messages_to_send = []
numberOfClients = 0
counters = dict()

print 'server is running!! waiting for clients...'
while True:
    rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, open_client_sockets, [])
    for current_socket in rlist:
        if current_socket == server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
            counters[new_socket] = [0, time.time()]
            numberOfClients += 1
            print "connected to IP: %s , port: %s. number of clients is %s \n" % (address[0], address[1], numberOfClients)
        else:
            try:
                data = current_socket.recv(1024)	
		if data == "":
		  open_client_sockets.remove(current_socket)
                  del counters[current_socket]
                  numberOfClients -= 1
                  print 'connection with a client is over. numebr of clients is {}\n'.format(str(numberOfClients))
		  break

		#enter code here
					
            except:
                numberOfClients -= 1
                open_client_sockets.remove(current_socket)
                print "connection was forcibly closed. number of clients is {}\n".format(str(numberOfClients))
                continue
            if data == "bye":
                open_client_sockets.remove(current_socket)
                del counters[current_socket]
                numberOfClients -= 1
                print 'connection with a client is over. numebr of clients is {}\n'.format(str(numberOfClients))
            else:
                messages_to_send.append((current_socket, 'dont know what to do'))

		#enter code here
    try:
        send_waiting_messages(wlist, messages_to_send)
    except:
        numberOfClients -= 1
        open_client_sockets.remove(current_socket)
        print "connection was forcibly closed. number of clients is {}\n".format(str(numberOfClients))
