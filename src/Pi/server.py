import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import scrypt
from random import *
import time

HOST = '127.0.0.1'
PORT = 65432
TIME_DELAY = 0.0002

test_keys = []
test_keys_ints = []
test_keys_opening_ints =[]
test_keys_opening = []

opening_keys_index = []
evaluation_keys_index = []

errors = []
counter = 0

# Decrypt message
def decrypt_message(key, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, test_keys[0]) # Using first test key as IV, needs to be random in future
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# Function to receive and decrypt messages from client
def receive_and_decrypt_message(conn, key):
    data = conn.recv(1024)
    ciphertext = pickle.loads(data)
    print("\nCiphertext: ", ciphertext, "\n")
    plaintext = decrypt_message(key, ciphertext)
    return plaintext


indices = sample(range(28), 28)
for i in range(14):
    opening_keys_index.append(indices[i])
    evaluation_keys_index.append(indices[i+14])

# Begin socket connection

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print("Server is listening for connections...")

        conn, addr = server_socket.accept()
        with conn:
            print('\nConnected by', addr, "\n")
            
            client_shares = ()

            # Begin initialization phase

            while True:
                data = conn.recv(1024)
                if data.endswith(b"READY"):
                    break
                shares_i = pickle.loads(data)
                client_shares += (shares_i,)
                #print(data, "\n")

            if len(client_shares) != 28:
                print("Error in initialization phase: Received", len(client_shares), "test keys instead of 28. Aborting protocol\n")
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()

            else:

                for i in range(28):
                    test_keys.append(Shamir.combine(client_shares[i]))
                    test_keys_ints.append(int.from_bytes(test_keys[i], 'big'))
                    #print("\nSecret ", i, ": ", test_keys[i])

                print("\nShares Received\n")

                # Begin cut and choose phase

                conn.sendall(pickle.dumps(opening_keys_index))
                conn.sendall(pickle.dumps(evaluation_keys_index))

                time.sleep(TIME_DELAY)
                conn.sendall(b"READY")

                print("Opening and Eval key indexes sent\n")

                client_shares_opening = ()
                while True:
                    data = conn.recv(1024)
                    if data.endswith(b"READY"):
                        break
                    shares_i = pickle.loads(data)
                    client_shares_opening += (shares_i,)

                if len(client_shares_opening) != 14:
                    print("Error in cut-and-choose phase: Received", len(client_shares_opening), "test keys instead of 14. Aborting protocol\n")
                    conn.shutdown(socket.SHUT_RDWR)
                    conn.close()

                else:
                    print("Received shares\n")

                    for i in range(14):
                        test_keys_opening.append(Shamir.combine(client_shares_opening[i]))
                        test_keys_opening_ints.append(int.from_bytes(test_keys_opening[i], 'big'))
                        if test_keys_ints[opening_keys_index[i]] != test_keys_opening_ints[i]:
                            print("Test Key at index ", opening_keys_index[i], " is not equal.\n")
                            errors.append(opening_keys_index[i])
                            print("Error at index: ", errors[counter], "\n")
                            counter += 1
                        #print("\nSecret ", i, ": ", test_keys[i])

                    print("Opening keys reconstructed!\n")

                    # Begin session key derivation phase

                    ciphertexts = []

                    data = conn.recv(1024)
                    ciphertexts = pickle.loads(data)

                    plaintexts = []
                    for i in range(14):
                        cipher = AES.new(test_keys[evaluation_keys_index[i]], AES.MODE_ECB)
                        plaintext = unpad(cipher.decrypt(ciphertexts[i]), AES.block_size)
                        plaintexts.append(plaintext)
                        #print("Secret: ", plaintexts[i])
                    
                    if len(plaintexts) != 0:
                        print("\nServer has received and decrypted ciphertexts. Calculating secret...\n")

                    secret = b'0'
                    for i in range(14):
                        if plaintexts[i] == plaintexts[i+1]:
                            secret = plaintexts[i]
                            break
                    if secret == 0:
                        print("Session Key Derivation Phase failed. Aborting protocol\n")
                        conn.shutdown(socket.SHUT_RDWR)
                        conn.close()

                    print("Calculated secret = ", secret, "\n")

                    key = scrypt(secret.decode(), "salt", 16, N=2**10, r=8, p=1) # TODO use random salt
                    print("Session Key: ", key)

                    # Begin communication with encrypted messages using derived key

                    while True:
                        plaintext = receive_and_decrypt_message(conn, key)
                        if plaintext == "quit":
                            print("Goodbye!\n")
                            conn.shutdown(socket.SHUT_RDWR)
                            conn.close()
                            break
                        print("Client ", addr, ":", plaintext)

    except Exception as e:
        print("\nError:", e, "\n")
