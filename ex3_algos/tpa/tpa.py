import socket
import threading
import time
import sys


class TokenRingNode:
    def __init__(self, port, next_host, next_port, has_token=False):
        self.port = port
        self.next_host = next_host
        self.next_port = next_port
        self.has_token = has_token
        self.request_cs = False
        self.running = True

    # -------------------- Networking --------------------
    def listen(self):
        """Listen for incoming token messages."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', self.port))
        server.listen(5)
        print(f"[{self.port}] Listening for token...")

        while self.running:
            try:
                conn, _ = server.accept()
                token = conn.recv(1024).decode()
                conn.close()

                if token == "TOKEN":
                    print(f"[{self.port}] Token received")
                    self.has_token = True
                    if self.request_cs:
                        self.enter_critical_section()
                    self.send_token()
            except Exception as e:
                print(f"[{self.port}] Error in listen: {e}")
            time.sleep(0.5)

    def send_token(self):
        """Send token to the next node in the ring."""
        if self.has_token:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.next_host, self.next_port))
                s.send("TOKEN".encode())
                s.close()
                print(f"[{self.port}] Token passed to {self.next_port}")
                self.has_token = False
            except Exception as e:
                print(f"[{self.port}] Failed to send token: {e}")

    # -------------------- Critical Section --------------------
    def enter_critical_section(self):
        """Simulate work inside CS."""
        print(f"[{self.port}] >>> Entering critical section...")
        time.sleep(3)  # simulate work
        print(f"[{self.port}] <<< Exiting critical section...")
        self.request_cs = False

    # -------------------- Lifecycle --------------------
    def start(self):
        """Start the node: listener thread + user interaction."""
        threading.Thread(target=self.listen, daemon=True).start()

        # If starting node already has token
        if self.has_token and self.request_cs:
            self.enter_critical_section()
            self.send_token()

        # User interaction loop
        while self.running:
            user_input = input(f"[{self.port}] Type 'request' to enter CS or 'exit' to quit: ").strip()
            if user_input == 'request':
                self.request_cs = True
            elif user_input == 'exit':
                self.running = False
                break

        print(f"[{self.port}] Shutting down...")


# -------------------- Main --------------------
if __name__ == "__main__":
    port = int(sys.argv[1])      # current node’s port
    next_port = int(sys.argv[2]) # next node’s port
    has_token = False

    if len(sys.argv) > 3:
        has_token = (sys.argv[3].lower() == "yes")

    node = TokenRingNode(port, 'localhost', next_port, has_token)
    node.start()

# -------------------- Code Run --------------------
# # Node 1 (first node has the token initially)
# python token_ring.py 9001 9002 yes

# # Node 2
# python token_ring.py 9002 9003

# # Node 3 (loops back to node 1)
# python token_ring.py 9003 9001
