from socket import *
import os
import threading
import sys
from termcolor import colored   #for highlighting

threads = []
clients = []
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
PROXY_SERV = '127.0.0.1'
PROXY_PORT = 8888
tcpSerSock.bind((PROXY_SERV,PROXY_PORT))
tcpSerSock.listen(5)
print(colored("[INFO] ",'green'),end="")
print(colored('Serving on Port '+str(PROXY_PORT),'white'))

def proxy(tcpCliSock, addr):
		while True:
			try:
				message =  tcpCliSock.recv(2048)
				if message.decode() != "":
					print(colored("[INFO] ",'green'),end="")
					print(colored("Message from ",'white'),end="")
					print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
					print(colored(' :- '+message.decode(),'white'))
					filename = message.decode()
					fileExist = "false"
					filepath = "www/" + filename
					arr = os.listdir("www")
					if filename in arr:
						print(colored("[INFO] ",'green'),end="")
						print(colored("File found in Proxy Server. Sending to "+str(addr[0])+':'+str(addr[1]),'white'))
						f = open(filepath,'r')
						data = f.read()
						tcpCliSock.send(data.encode())
					else:
						print(colored("[INFO] ",'green'),end="")
						print(colored("File not found in Proxy Server. Requesting from Server",'yellow'))
						server = socket(AF_INET, SOCK_STREAM)
						server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
						try:
							server.connect(("127.0.0.1",8081))
							print(colored("[INFO] ",'green'),end="")
							print(colored("Connected to Server. Fetching from server",'white'))
							server.send(filename.encode())
							data = server.recv(2048)
							print(colored("[INFO] ",'green'),end="")
							print(colored(filename+" found in Server. Sending to "+str(addr[0])+':'+str(addr[1]),'white'))
							tcpCliSock.send(data)
							server.send("exit".encode())	#disconnect from server
							server.close()
							if "Nil" not in data.decode():
								print(colored("[INFO] ",'green'),end="")
								print(colored("Writing "+filename+"to Proxy Server",'yellow'))
								w = open(filepath,'w')
								w.write(data.decode())
								w.close()

						except:
							tcpCliSock.send("Unable to connect to Server".encode())
							print(colored("[INFO] ",'green'),end="")
							print(colored("Unable to connect to Server",'yellow'))
				else:
					continue
				
			except Exception as e:
				break

def shutdown():
	while True:
		cmd = input()
		if cmd == "quit":
			print(colored("[INFO] ",'green'),end="")
			print(colored("Shutdown signal recieved",'yellow'))
			tcpSerSock.close()
			for client in clients:
				client.send("exit".encode())
				client.close()
			break
		else:
			continue

sd = threading.Thread(target=shutdown)
sd.start()

while True:
	try:
		tcpCliSock, addr = tcpSerSock.accept()
		clients.append(tcpCliSock)
		print(colored("[INFO] ",'green'),end="")
		print(colored(str(addr[0])+':'+str(addr[1]),'cyan'),end="")
		print(colored(' connected','white'))
		t = threading.Thread(target=proxy, args=(tcpCliSock,addr))
		threads.append(t)
		t.start()
	except:
		break

for t in threads:
    t.join()

sd.join()
print(colored("[SHUTDOWN] ",'green'),end="")
print(colored("Proxy Server has shutdown",'white'))
