import socket 
import threading
import random

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'ascii'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []

def isPrime(x):
    count = 0
    for i in range(int(x/2)):
        if x % (i+1) == 0:
            count = count+1
    return count == 1

primes = [i for i in range(2,9997) if isPrime(i)]

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected but not secured.")

    prime = random.choice(primes)
    base = random.randrange(2,9997)
    while base == prime :
        base = random.randrange(2,9997)

    #prime=29
    #base=5

    conn.send(f"\nConnection established but not secured. Let's make it secure! \n\nPrime = {prime}, Base = {base}\n". encode(FORMAT))
    
    count = 1
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            msg_length = int(msg)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "!DISCONNECT":
                print(f"[{addr}] {msg}")
                connected = False
                break
            print(f"[{addr}] {msg}")
            if count==1:
                private_key = int(input("Enter your private key : "))
                sendable_number = (base ** private_key) % prime
                print("\nnumber sent = ",sendable_number)
                sendable_number = str(sendable_number)
                conn.send(sendable_number.encode(FORMAT))
                sendable_number = int(sendable_number)
                received_number = int(msg)
                final_private_key = (received_number ** private_key) % prime
                while final_private_key == prime or final_private_key == base or final_private_key == sendable_number or final_private_key == received_number :
                    print(f"\nKey = {final_private_key}\n\nThere was a security issue. re-establishing connection...\n")
                    handle_client(conn, addr)
                print("final private key = ",final_private_key)
            conn.send(input().encode(FORMAT))
        count+=1
    conn.close()

def start():
    server.listen(2)
    print(f"[LISTENING] Server is listening on {SERVER}")
    server_connected = True
    while server_connected:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        server_connected = False

print("[STARTING] server is starting...")
start()