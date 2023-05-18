import socket

HEADER = 64
PORT = 5050
FORMAT = 'ascii'
msg = ""
SERVER = "192.168.0.103"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def security():
    print(client.recv(2048).decode(FORMAT))
    prime= int(input("Enter prime = "))
    base = int(input("Enter base = "))
    private_key = int(input("Enter your private key = "))
    sendable_number = (base ** private_key) % prime
    sendable_number = str(sendable_number)
    send(sendable_number)
    print("number sent = ", sendable_number)
    received_number = client.recv(2048).decode(FORMAT)
    print("received number = ",received_number)
    received_number = int(received_number)
    final_private_key = (received_number ** private_key) % prime
    while final_private_key == prime or final_private_key == base or final_private_key == sendable_number or final_private_key == received_number :
        print(f"\nKey = {final_private_key}\n\nThere was a security issue. re-establishing connection...")
        security()
    print("final private key = ",final_private_key)

count = 1
while msg != "!DISCONNECT":
    if count == 1:
        security()
    print(client.recv(2048).decode(FORMAT))
    msg = input()
    send(msg)
    count += 1