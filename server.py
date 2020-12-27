#multiple instances of python code
import socket
import threading

#threading is a way of creatign mutiple threads within 1 python program
#all message handling stuff is in each thread so each thread can communicate with the server 
HEADER = 64
#first message from the client is going to be header of length 64
PORT = 5050
#need to pick a port on server to run on
#typically 10,000 ports over 4000 are normally free but check!
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


#SERVER = "192.168.0.25"
#couple of options, either do ipconfig
#or get the IP address of the computer by name - gethostname gets your computer name on the network
SERVER = socket.gethostbyname(socket.gethostname())
#print(SERVER)
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#make a new socket, first arguement is the family of scoket - what type of address are we accepting/ looking for when connecting
#second is just way fo sending data through socket - we are just streaming. This can be a complex topic!

#now we need to bind, but arguments need to be in a tuple
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT) #blocking line of code - won't pass this line of code untill recieve a message from client - hence threads
        #64 is quite small - if message is very large - header might be too small to represent length of message
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Message Recieved".encode(FORMAT)) #after recieve a message confirm it
    
    conn.close()


def start():
    server.listen() #listen for new connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept() #this line will wait and save info abotu connection
        #now we will start a thread and handle individual connectin between client and server
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS], {threading.activeCount()-1}") #active connections = number of threads (-1 as first instance is also a connection)

print("Server is starting....")
start()

#if you want to send objects and receiev objects - either used pickle or json serialise it