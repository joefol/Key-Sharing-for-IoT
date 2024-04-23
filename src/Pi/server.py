import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is listening for connections...")

    conn, addr = server_socket.accept()
    with conn:
        print('\nConnected by', addr)

        # Start pi
        client_shares = conn.recv(1028)
        client_shares = pickle.loads(client_shares)

        secret = Shamir.combine(client_shares)
        secret = int.from_bytes(secret, 'big')

        print("\nSecret: ", secret)