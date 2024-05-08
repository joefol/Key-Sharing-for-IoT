import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir
from random import *
import time

HOST = '127.0.0.1'
PORT = 65432

opening_keys_index = []
evaluation_keys_index = []


# Needs to be random, doing 0-13 for opening keys and 14-27 for eval keys
for i in range(14):
    opening_keys_index.append(i)
    evaluation_keys_index.append(i+14)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Server is listening for connections...")

        conn, addr = server_socket.accept()
        with conn:
            print('\nConnected by', addr, "\n")
            
            client_shares = ()

            data = conn.recv(2048)
            while data:
                shares_i = pickle.loads(data)
                client_shares += (shares_i,)
                data = conn.recv(2048)

            print("Check")
            if len(client_shares) != 28:
                print("Error: Received", len(client_shares), "test keys instead of 28.\n")

            else:
                #print(client_shares)
                test_keys = []

                for i in range(28):
                    test_keys.append(Shamir.combine(client_shares[i]))
                    test_keys[i] = int.from_bytes(test_keys[i], 'big')
                    #print("\nSecret ", i, ": ", test_keys[i])

                print("\nShares Received\n")

                conn.sendall(pickle.dumps(opening_keys_index))
                conn.sendall(pickle.dumps(evaluation_keys_index))

                print("Opening and Eval key indexes sent\n")

                #TODO Receive next set of shares from client

    except Exception as e:
        print("\nError:", e, "\n")
