import socket
from Crypto.PublicKey import RSA
import time

# Client Configuration
HOST = '127.0.0.1'
PORT = 65432

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    start_time = time.time()

    client_key = RSA.generate(3072)
    client_public_key = client_key.public_key().export_key()

    client_socket.sendall(client_public_key)

    server_public_key_bytes = client_socket.recv(3072)
    server_public_key = RSA.import_key(server_public_key_bytes)

    end_time = time.time() - start_time

    print("\nServer's public key: ", server_public_key)
    print("\nTime to receive server's public key: ", end_time, "\n")