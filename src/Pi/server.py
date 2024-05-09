import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir
from random import *
import time

HOST = '127.0.0.1'
PORT = 65432
TIME_DELAY = 0.0002

opening_keys_index = []
evaluation_keys_index = []
test_keys_opening = []
errors = []
counter = 0


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

            while True:
                data = conn.recv(1024)
                if data.endswith(b"READY"):
                    print("BREAK\n")
                    break
                shares_i = pickle.loads(data)
                client_shares += (shares_i,)
                #print(data, "\n")

            print("continuing\n")
            if len(client_shares) != 28:
                print("Error in initialization phase: Received", len(client_shares), "test keys instead of 28. Aborting protocol\n")
                server_socket.close()

            else:
                #print(client_shares)
                test_keys = []

                for i in range(28):
                    test_keys.append(Shamir.combine(client_shares[i]))
                    test_keys[i] = int.from_bytes(test_keys[i], 'big')
                    print("\nSecret ", i, ": ", test_keys[i])

                print("\nShares Received\n")

                conn.sendall(pickle.dumps(opening_keys_index))
                conn.sendall(pickle.dumps(evaluation_keys_index))

                time.sleep(TIME_DELAY)
                conn.sendall(b"READY")

                print("Opening and Eval key indexes sent\n")

                #TODO Receive next set of shares from client
                # Need to adjust
                # Server_socket.shutdown(socket.SHUT_RD)

                client_shares_opening = ()
                while True:
                    data = conn.recv(1024)
                    if data.endswith(b"READY"):
                        break
                    shares_i = pickle.loads(data)
                    client_shares_opening += (shares_i,)

                if len(client_shares_opening) != 14:
                    print("Error in cut-and-choose phase: Received", len(client_shares_opening), "test keys instead of 14. Aborting protocol\n")
                    server_socket.close()

                else:
                    print("Received shares\n")
                    #print(client_shares)

                    for i in range(14):
                        test_keys_opening.append(Shamir.combine(client_shares_opening[i]))
                        test_keys_opening[i] = int.from_bytes(test_keys_opening[i], 'big')
                        if test_keys[i] != test_keys_opening[i]:
                            print("Test Key at index ", opening_keys_index[i], " is not equal.")
                            errors.append(opening_keys_index[i])
                            print("Error at index: ", errors[counter])
                            counter += 1
                        print("\nSecret ", i, ": ", test_keys[i])

                    #print("\nShares Received\n")

    except Exception as e:
        print("\nError:", e, "\n")
