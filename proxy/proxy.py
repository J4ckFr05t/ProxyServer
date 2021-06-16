from socket import *
import os
import threading
import sys
from termcolor import colored   #for highlighting

if len(sys.argv) <= 1:
	print(colored("[INFO] ",'green'),end="")
	print(colored('Usage : "python3 proxy.py ProxyServerIP"','white'))
	sys.exit(2)

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
				print(colored("[INFO] Message from ",'white'),end="")
				print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
				print(colored(' :- '+message.decode(),'white'))
				filename = message.decode()
				fileExist = "false"
				filepath = "www/" + filename
				arr = os.listdir("www")
				if filename in arr:
					print(colored("[INFO] ",'green'),end="")
					print(colored("file found in Proxy Server",'white'))
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
						tcpCliSock.send(data)
						server.send("exit".encode())	#disconnect from server
						server.close()
						if "Nil" not in data.decode():
							print(colored("[INFO] ",'green'),end="")
							print(colored("Writing file to Proxy Server",'yellow'))
							w = open(filepath,'w')
							w.write(data.decode())
							w.close()

					except:
						tcpCliSock.send("Unable to connect to Server".encode())
				
			except:
				break

while True:
	try:
		tcpCliSock, addr = tcpSerSock.accept()
		print(colored("[INFO] ",'green'),end="")
		print(colored(str(addr[0])+':'+str(addr[1]),'cyan'),end="")
		print(colored(' connected','white'))
		th = threading.Thread(target=proxy, args=(tcpCliSock,addr))
		th.start()
	except KeyboardInterrupt:
		tcpSerSock.flush()
		tcpSerSock.close()