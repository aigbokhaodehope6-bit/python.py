import socket
import datetime

# Configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 2222       # Your honeyport
LOG_FILE = 'honeyport_log.txt'

# Setup socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[INFO] Honeyport running on port {PORT}...")

while True:
    client, addr = server.accept()
    ip = addr[0]
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Log connection
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - Connection from {ip}\n")
    
    print(f"[ALERT] {timestamp} - Connection from {ip}")
    
    # Fake service response
    client.send(b"Welcome to your honeyport!\n")
    client.close()
