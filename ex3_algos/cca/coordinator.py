import socket
import threading 
from queue import Queue 

HOST = "localhost"
PORT = 12345
MAXBYTES = 1024

cNo = 0
lock = threading.Lock()
reqQueue = Queue()
inCS = False

def handleClient(c, addr):
    global cNo, inCS

    cNo += 1
    print(f"[+ Client {cNo}]: Connected by {addr}")
    while True: 
            try:
                msg = c.recv(MAXBYTES).decode()
                if not msg:
                    break

                if msg == "REQ_CS":
                      print(f"[Client {cNo}]: Requesting CS...")
                      with lock:
                           reqQueue.put(c)
                           processQueue()

                elif msg == "REL_CS":
                     print(f"[Client {cNo}]: Releasing CS...")
                     with lock:
                          inCS = False 
                          processQueue()
            
            except:
                 break 
    c.close()

def processQueue():
     global inCS

     if not inCS and not reqQueue.empty():
        c = reqQueue.get()
        inCS = True
        c.sendall("GRANT_CS".encode())

def startServer():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Server]: listening to port {PORT}...")

    while True:
        c, addr = s.accept()
        threading.Thread(target=handleClient, args=(c, addr)).start()

if __name__ == "__main__":
    startServer()