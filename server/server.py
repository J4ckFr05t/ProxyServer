import socket
import sys
import os
from _thread import *
import threading
import time
from termcolor import colored   #for highlighting

working_dir = os.getcwd()+'/www/'
print(colored("[DEBUG] ",'green'),end="")
print(colored("Public Directory : "+working_dir,'yellow'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    IP_address = "127.0.0.1"
    Port = 8081
except:
    print(colored("[INFO] ",'green'),end="")
    print(colored(" Unable to start server. Try changing the port"),'white')
    sys.exit()

all_threads = [] 
server.bind((IP_address, Port))
print(colored("[INFO] ",'green'),end="")
print(colored("Server running on port "+str(Port),'white'))
server.listen(100) 
list_of_clients = [] 
  
def clientthread(conn, addr):
    while True: 
            try: 
                message = conn.recv(2048)
                if message.decode() == "exit":
                    print(colored("[INFO] ",'green'),end="")
                    print(colored(str(addr[0])+":"+str(addr[1]),'cyan'),end="")
                    print(colored(" left the server",'white'))
                    esms = "exit"
                    remove(conn)
                    break

                elif message.decode() == "quit":
                    print(colored("[SHUTDOWN] ",'green'),end="")
                    print(colored("Got shutdown signal",'white'))
                    server.close()
                    break

                else:
                    send(message.decode(), conn, addr)
  
            except: 
                continue

def send(fiLe, connection, address):
    arr = os.listdir(working_dir)
    file_path = working_dir+fiLe
    try:
        if fiLe in arr:
            f = open(file_path,'r')
            content = f.read()
            f.close()
            msg = content
            print(colored("[SEND] ",'green'),end="")
            print(colored("Sending requested file to "+str(address[0])+":"+str(address[1]),'white'))
            connection.send(msg.encode())
        else:
            connection.send("Nil".encode())
    except Exception as e:
        print(colored("[Exception] ",'green'),end="")
        print(colored("Unable to open file !",'white'))
        print(colored(e,'red'))

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection)

"""
def shutdown():
    while True:
        cmd = input()
        if cmd == "quit":
            server.close()
            break
        else:
            print("Server Running")
"""

#sd = threading.Thread(target=shutdown)
#sd.start()
  
while True:
    try:
        conn, addr = server.accept() 
        list_of_clients.append(conn)
        print(colored("[INFO] ",'green'),end="")
        print(colored(str(addr[0])+":"+str(addr[1]),'white'))
        t=threading.Thread(target=clientthread,args=(conn,addr))
        all_threads.append(t)
        t.start()
    except:
        break

for th in all_threads:
    th.join()

#sd.join()
print(colored("[INFO] ",'green'),end="")
print(colored("Server has shutdown",'white'))