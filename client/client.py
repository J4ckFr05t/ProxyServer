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

def read():
	while True:
		try:
			message=input("Enter filename\t: ")
			if message == 'exit':
				break
			else:
				msg = message
				sock.send(msg.encode())
		except KeyboardInterrupt:
			break

def fetch():
	while True:
		message = sock.recv(2048)
		if message.decode() == "quit":
			print("Server shutting down. Type exit\n$:",end="")
			break
		elif message.decode() == "exit":
			print("\nBye")
			break
		else:
			print(colored("\n"+message.decode(),'cyan'))
			print('\nEnter filename\t: ',end="")
	
	
t1 = threading.Thread(target =  read)
t1.start()
t2 = threading.Thread(target = fetch)
t2.start()

t1.join()
t2.join()
sock.close()