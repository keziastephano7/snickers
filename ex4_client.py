import socket
import time
import random # Used to simulate a local clock that is slightly fast/slow

# Client Configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
CLIENT_PORT = 54321 # Client needs its own port for response

def start_time_client():
    """Simulates a client requesting time and calculating offset."""
    try:
        # 1. Initialize Client Clock (simulate a small initial error)
        # We simulate the local clock being off by up to +/- 1000 milliseconds (1 second)
        initial_offset_ms = random.randint(-1000, 1000)
        
        # NOTE: In a real system, the OS manages the clock. Here, we use 'time.time()'
        # as the baseline and simulate the 'local_time' by adding an offset.
        def get_local_time():
            return (time.time() * 1000) + initial_offset_ms

        print(f"Local Clock initialized with error: {initial_offset_ms} ms")
        print(f"Local Time (Before Sync): {get_local_time():.4f} ms\n")
        
        # 2. Setup UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind client to its port (optional, but good practice)
        client_socket.bind(('', CLIENT_PORT))
        client_socket.settimeout(5)

        # 3. Send Request and Record T1 (Client Transmit)
        # T1 is the time the client sends the request.
        T1 = get_local_time()
        request_message = "GIVE_ME_TIME".encode('utf-8')
        
        client_socket.sendto(request_message, (SERVER_IP, SERVER_PORT))
        print(f"⬆️ Client Request Sent at T1: {T1:.0f} ms")

        # 4. Receive Response and Record T4 (Client Receive)
        data, server_address = client_socket.recvfrom(1024)
        T4 = get_local_time()
        
        # The received data is the server's time (T_server). We treat this as T3.
        # Since this is a simple simulation, we assume T2 is very close to T3.
        T_server = int(data.decode('utf-8'))
        
        print(f"⬇️ Server Time Received (T3): {T_server} ms")
        print(f"Client Response Received at T4: {T4:.0f} ms\n")

        # 5. Calculate Offset
        
        # Calculate Round-Trip Delay (Latency)
        # Latency = T4 (Client Receive) - T1 (Client Transmit)
        latency = T4 - T1
        
        # Estimated One-Way Trip Time
        one_way_delay = latency / 2
        
        # Calculate Clock Offset (how far ahead/behind the client is)
        # Offset (θ) = Server Time (T_server) - Client's adjusted time (T1 + one_way_delay)
        clock_offset = T_server - (T1 + one_way_delay)
        
        # 6. Apply Synchronization
        synchronized_time = get_local_time() + clock_offset
        
        # 7. Print Results
        print("--- Synchronization Results ---")
        print(f"Round-Trip Latency (δ): {latency:.2f} ms")
        print(f"Calculated Clock Offset (θ): {clock_offset:.2f} ms")
        print(f"Local Time (Before Sync): {get_local_time():.0f} ms")
        print(f"Synchronized Time (Adjusted): {synchronized_time:.0f} ms")
        print(f"Time difference fixed by: {abs(clock_offset):.2f} ms")
        
    except socket.timeout:
        print("❌ Error: Request timed out. Server might not be running or is unresponsive.")
    except ConnectionRefusedError:
        print("❌ Error: Connection refused. Ensure the server script is running.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        client_socket.close()

if _name_ == "_main_":
    start_time_client()
