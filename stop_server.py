from _thread import *
import sys
import threading
import socket
from termcolor import colored   #for highlighting

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	sock.connect(('127.0.0.1',8081))
	print(colored("[INFO] ",'green'),end="")
	print(colored("connected to Server",'white'))
except Exception as e:
	print(colored("[INFO] ",'green'),end="")
	print(colored("Server is down",'white'))
	sys.exit()

def stopper():
	while True:
		try:
			msg="quit"
			sock.send(msg.encode())
			print(colored("[INFO] ",'green'),end="")
			print(colored("Server has shutdown successfully",'cyan'))
			break

		except Exception as e:
			print("Unable to connect")
			break

	
stopper()
sock.close()