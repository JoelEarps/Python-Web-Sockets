import socket


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.25"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#client needs to connect to a socket and nto bind to it like the server
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    #so we send the message length first as the header file buth then pad it to make it 64 in length
    send_length += b' ' * (HEADER - len(send_length)) #so we look at the length of the message, 64 - that length is the number of padded spaces needed
    #bite space
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World")
raw_input() #enter to send, python 3 is just input
send("Hello World 2")
raw_input()
send("Hello World  3")
send(DISCONNECT_MESSAGE)



