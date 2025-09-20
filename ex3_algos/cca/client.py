import socket 
import time 

HOST = "localhost"
PORT = 12345
MAXBYTES = 1024


def connectClient():
    s = socket.socket()
    s.connect((HOST, PORT))
    print(f"[Client]: connected to {HOST} via {PORT}...")

    while True:
        print("[Client]: requesting CS...")
        s.sendall("REQ_CS".encode())

        res = s.recv(MAXBYTES).decode()
        if res == "GRANT_CS":
            print("[Client]: entering CS...")
            time.sleep(3)
            print("[Client]: leaving CS...")
            s.sendall("REL_CS".encode())
            

if __name__ == "__main__":
    connectClient()