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

        client_shares = ()

        while True:
            data = conn.recv(50000)
            if len(client_shares) == 28:
                break
            test = pickle.loads(data)
            client_shares += (test,)

        if len(client_shares) != 28:
            print("Error: Received", len(client_shares), "test keys instead of 28.")
        else:
            test_keys = []

            for i in range(28):
                test_keys.append(Shamir.combine(client_shares[i]))
                test_keys[i] = int.from_bytes(test_keys[i], 'big')
                print("\nSecret ", i, ": ", test_keys[i])

        # Do cut and choose phase

        '''
        # Start pi
        client_shares = conn.recv(128)
        client_shares = pickle.loads(client_shares)

        secret = Shamir.combine(client_shares)
        secret = int.from_bytes(secret, 'big')

        print("\nSecret: ", secret)
        '''
