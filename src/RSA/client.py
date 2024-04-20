import socket

# Client Configuration
HOST = '127.0.0.1'
PORT = 65432

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))