import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    # Start pi
    secret = 28
    print("\nSecret: ", secret)
    shares = Shamir.split(4, 6, secret)
    data = pickle.dumps(shares)

    client_socket.sendall(data)
