from _thread import *
import sys
import threading
import socket
from termcolor import colored   #for highlighting

if len(sys.argv) < 2:
	#print(colored("[INFO] ",'green'),end="")
	#print(colored("Usage : python3 one_way_client.py <filename>",'white'))
	sys.exit()
else:
	filename = sys.argv[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	sock.connect(('127.0.0.1',8888))
	#print(colored("[INFO] ",'green'),end="")
	#print(colored("connected to File Server\n",'white'))
except Exception as e:
	#print(colored("[INFO] ",'green'),end="")
	print("Unable to connect to File Server\n")
	sys.exit()

def client(filename):
	while True:
		try:
			message=filename
			if message == 'exit':
				break
			elif message == "":
				break
			else:
				msg = message
				sock.send(msg.encode())

				message = sock.recv(2048)
				if message.decode() == "exit":
					print("Lost connection with Proxy Server")
				else:
					print(message.decode())

				sock.close()
				break

		except Exception as e:
			print("Unable to connect")
			break

client(filename)