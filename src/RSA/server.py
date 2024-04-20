import socket
from Crypto.PublicKey import RSA

# Server Configuration
HOST = '127.0.0.1'
PORT = 65432

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is listening for connections...")

    # Accept connection
    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)

        server_key = RSA.generate(3072)
        server_public_key = server_key.public_key().export_key()

        conn.sendall(server_public_key)

        client_public_key_bytes = conn.recv(3072)
        client_public_key = RSA.import_key(client_public_key_bytes)

        print("\nClient's public key: ", client_public_key, "\n")
