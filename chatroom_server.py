import socket 
import select 
import sys
# import client
# from client import *
from thread import *

  
"""AF_INET is the address domain of the socket.
SOCK_STREAM means that data or characters are read in continuously."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP_address = str('127.0.0.1') 
Port = int(4000) 
  
 
# binds the server IP address and at the port number. 

server.bind((IP_address, Port)) 
 
# Allow up to 500 connections
server.listen(500) 
  
list_of_clients = [] 
  
def clientthread(conn, name): 
  
    # sends a welcome message to the client that connects 
    conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
  
                    """prints the message and address of the 
                    user who recently sent the message to the server 
                    terminal"""
                    # print client.name + message 
                    print "<" + name[0] + "> " + message 
  
                    # Calls broadcast  to send message to everyone 
                    message_to_send = "<" + name[0] + "> " + message 
                    broadcast(message_to_send, conn) 
  
                else: 
                    """message may have no content if the connection 
                    is broken then we remove the connection"""
                    remove(conn) 
  
            except: 
                continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                print clients.name
                clients.send(message) 
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients) 
  
"""The following functionremoves the object 
from the list that was created at the beginning of  
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address of the client that just  
    connected"""
    conn, addr = server.accept() 
  
    """Maintains a list of clients"""
    list_of_clients.append(conn) 
    """ Take the name first and then take a map between the connection id and the name"""
  
    # prints the address of the user that just connected 
    print name[0] + " connected"
  
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,(conn,addr,name))     
  
conn.close() 
server.close() 