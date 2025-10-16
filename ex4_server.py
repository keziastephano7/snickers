import socket
import time
import sys

# Server Configuration
SERVER_IP = '127.0.0.1' # Localhost
SERVER_PORT = 12345     # A simple, high-numbered port

def start_time_server():
    """Starts a simple UDP server to send its current time upon request."""
    try:
        # Create a UDP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to the IP and port
        server_socket.bind((SERVER_IP, SERVER_PORT))
        
        print(f"✅ Time Server is running on {SERVER_IP}:{SERVER_PORT}")
        print("Waiting for client request...")

        while True:
            # Receive data and client address
            data, client_address = server_socket.recvfrom(1024)
            
            # Record the server's transmit time (T_server)
            server_time_s = time.time()
            server_time_ms = int(server_time_s * 1000) # Time in milliseconds
            
            # The server sends its timestamp back as a string
            response_data = str(server_time_ms).encode('utf-8')
            
            # Send the time back to the client
            server_socket.sendto(response_data, client_address)
            
            print(f"🕰️ Sent local time {server_time_ms} ms to client {client_address}")

    except KeyboardInterrupt:
        print("\nServer shutting down.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        server_socket.close()

if _name_ == "_main_":
    start_time_server()
