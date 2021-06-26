from socket import *
import os
import threading
import sys
from termcolor import colored   #for highlighting
import logging 

#now we will Create and configure logger 
logging.basicConfig(filename="proxy.log", 
					format='%(asctime)s %(message)s', 
					filemode='w') 

#Let us Create an object 
logger=logging.getLogger() 

#Now we are going to Set the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG)

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
logger.debug("Server running on port "+str(PROXY_PORT))

def proxy(tcpCliSock, addr):
		while True:
			try:
				message =  tcpCliSock.recv(2048)
				if message.decode() == "quit":
					logger.debug("Closing Proxy Server socket")
					tcpSerSock.close()
					for client in clients:
						client.send("exit".encode())
						client.close()
					break
					
				elif message.decode() != "":
					print(colored("[INFO] ",'green'),end="")
					print(colored("Message from ",'white'),end="")
					print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
					print(colored(' :- '+message.decode(),'white'))
					filename = message.decode()
					fileExist = "false"
					filepath = "p_www/" + filename
					logger.debug(str(addr[0])+":"+str(addr[1])+" Requesting "+filepath)
					arr = os.listdir("p_www")
					if filename in arr:
						print(colored("[INFO] ",'green'),end="")
						print(colored(filename+" found in Proxy Server. Sending to "+str(addr[0])+':'+str(addr[1]),'white'))
						logger.debug(filename+" found in Proxy Server. Sending to "+str(addr[0])+':'+str(addr[1]))
						f = open(filepath,'r')
						data = f.read()
						tcpCliSock.send(data.encode())
					else:
						print(colored("[INFO] ",'green'),end="")
						print(colored("File not found in Proxy Server. Requesting from Server",'yellow'))
						logger.info(filepath+" not found in Proxy Server. Requesting from Server")
						server = socket(AF_INET, SOCK_STREAM)
						server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
						try:
							server.connect(("127.0.0.1",8081))
							print(colored("[INFO] ",'green'),end="")
							print(colored("Connected to Server. Fetching from server",'white'))
							logger.info("Connected to Server. Fetching "+filename+" from server")
							server.send(filename.encode())
							data = server.recv(2048)
							if data.decode() != 'Nil':
								print(colored("[INFO] ",'green'),end="")
								print(colored(filename+" found in Server. Sending to "+str(addr[0])+':'+str(addr[1]),'white'))
								tcpCliSock.send(data)
							else:
								print(colored("[INFO] ",'green'),end="")
								print(colored(filename+" not found in Server.",'yellow'))
								logger.info(filename+" not found in Server.")
								tcpCliSock.send("File not found".encode())

							server.send("exit".encode())	#disconnect from server
							server.close()
							if "Nil" not in data.decode():
								print(colored("[INFO] ",'green'),end="")
								print(colored("Writing "+filename+"to Proxy Server",'yellow'))
								logger.debug("Writing "+filepath+" to Proxy Server")
								w = open(filepath,'w')
								w.write(data.decode())
								w.close()

						except Exception as e:
							tcpCliSock.send("Unable to fetch file / file not found".encode())
							print(colored("[INFO] ",'green'),end="")
							print(colored("Unable to connect to Server",'yellow'))
							logger.info("Unable to fetch file / file not found")
							logger.error(e)

				else:
					continue
				
			except Exception as e:
				logger.warning("something went wrong")
				logger.error(e)
				break

while True:
	try:
		tcpCliSock, addr = tcpSerSock.accept()
		clients.append(tcpCliSock)
		print(colored("[INFO] ",'green'),end="")
		print(colored(str(addr[0])+':'+str(addr[1]),'cyan'),end="")
		print(colored(' connected','white'))
		logger.info(str(addr[0])+':'+str(addr[1])+" connected")
		t = threading.Thread(target=proxy, args=(tcpCliSock,addr))
		threads.append(t)
		t.start()
	except:
		logger.warning("Shutting down")
		break

for t in threads:
    t.join()

print(colored("[SHUTDOWN] ",'green'),end="")
print(colored("Proxy Server has shutdown",'white'))
logger.info("Server has shutdown")
