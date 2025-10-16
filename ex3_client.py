import socket, threading 

host = "localhost"
port = 12345
maxbytes = 1024

def sendMsg(s):
    while True:
        msg = input("")
        s.sendall(msg.encode())
        if msg == "exit":
            s.close()
            break 

def recvMsg(s):
    try:
        while True:
            reply = s.recv(maxbytes).decode()
            if not reply:
                break 
            print(f"{reply}\n")
    except:
        print("\nYou have left the chat.")

def connectClient():
    s = socket.socket()
    s.connect((host, port))
    print(f"You have entered the chat.")
    print(f"(Type exit to leave chat).\n")

    threading.Thread(target=sendMsg, args=(s,)).start()
    threading.Thread(target=recvMsg, args=(s,)).start()

if __name__ == "__main__":
    connectClient()
