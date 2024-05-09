import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Cipher import AES
import time
from random import randbytes

HOST = '127.0.0.1'
PORT = 65432

TIME_DELAY = 0.0002

test_keys = []
test_key_shares = []

# 28 test keys
# generate 28 test keys of size 128-bit for AES encryption/decryption
# split each test keys into 6 shares, need 4 to reconstruct, and send to server
for i in range(28):
    key = randbytes(16)
    test_keys.append(key)

for i in range(28):
    test_key_shares.append(Shamir.split(4, 6, test_keys[i]))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))

        print("\nSuccessfully Connected to Server!\n")
        
        for i in range(28):
            data = pickle.dumps(test_key_shares[i])
            client_socket.sendall(data)
            time.sleep(TIME_DELAY)
        time.sleep(TIME_DELAY)
        client_socket.sendall(b"READY")

        print("\nshares sent\n")
        #client_socket.shutdown(socket.SHUT_WR)

        # Receive opening key and evaluation key indices
        indices = []
        while True:
            data = client_socket.recv(1024)
            if data.endswith(b"READY"):
                #print("BREAK\n")
                break
            indices += pickle.loads(data)

        if len(indices) != 0:
            print(len(indices), " Indices received\n")
        else: 
            print("Error in initialization phase, aborting protocol\n")

        #TODO Continue 2nd half of cut and choose phase

        opening_key_indices = indices[:14]
        eval_key_indices = indices[14:]

        '''
        for i in range(14):
            print("Opening indices: ", opening_key_indices[i], "\n")
            print("Eval indices: ", eval_key_indices[i], "\n")
        '''
        
        print("Indices received from server\n")

        for i in range(14):
            data = pickle.dumps(test_key_shares[opening_key_indices[i]])
            client_socket.sendall(data)
            #print("Check\n")
            time.sleep(TIME_DELAY)

        data = b"READY"
        client_socket.sendall(data)

        print("Sent opening key shares to server\n")

    except Exception as e:
        print("\nError: ", e, "\n")