import socket, threading 

host = "localhost"
port = 12345
maxbytes = 1024

clients = []

def handleClient(conn, addr):
    print(f"[+] Client {addr} joined.")
    clients.append(conn)

    while True:
            msg = conn.recv(maxbytes).decode()
            formattedMsg = f"\n{addr}: {msg}"

            if msg == "exit":
                print(f"[-] Client {addr} left.")
                clients.remove(conn)
                break 

            for client in clients:
                if client != conn:
                    client.sendall(formattedMsg.encode())
    conn.close()
        

def startServer():
    s = socket.socket()
    s.bind((host, port))
    s.listen()
    print(f"[Server]: Listening to {port}..")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handleClient, args=(conn,addr)).start()

if __name__ == "__main__":
    startServer()   