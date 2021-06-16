from _thread import *
import sys
import threading
import socket
from termcolor import colored   #for highlighting

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
	sock.connect(('127.0.0.1',8888))
	print(colored("[INFO] ",'green'),end="")
	print(colored("connected to File Server\n",'white'))
except Exception as e:
	print(colored("[INFO] ",'green'),end="")
	print(colored("Unable to connect to File Server\n",'white'))
	sys.exit()

def client():
	while True:
		try:
			message=input("Enter filename\t: ")
			if message == 'exit':
				break
			elif message == "":
				continue
			else:
				msg = message
				sock.send(msg.encode())

				message = sock.recv(2048)
				print(colored("\n"+message.decode(),'cyan'))

		except KeyboardInterrupt:
			break

	
t1 = threading.Thread(target =  client)
t1.start()

t1.join()
sock.close()