import socket
import pickle
from Crypto.Protocol.SecretSharing import Shamir
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Protocol.KDF import scrypt
import time
from random import randbytes

HOST = '127.0.0.1'
PORT = 65432

TIME_DELAY = 0.0002

test_keys = []
test_key_shares = []

# Encrypt message

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC, test_keys[0]) # Using first test key as IV, needs to be random in future
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    print("\nCiphertext: ", ciphertext, "\n")
    return ciphertext

# Function to send encrypted message to server

def send_encrypted_message(client_socket, key, message):
    ciphertext = encrypt_message(key, message)
    data = pickle.dumps(ciphertext)
    client_socket.sendall(data)

# 28 test keys
# generate 28 test keys of size 128-bit for AES encryption/decryption
# split each test keys into 6 shares, need 4 to reconstruct, and send to server

for i in range(28):
    key = randbytes(16)
    test_keys.append(key)

for i in range(28):
    test_key_shares.append(Shamir.split(4, 6, test_keys[i]))

# Beginning socket connection to server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    try:
        client_socket.connect((HOST, PORT))

        print("\nSuccessfully Connected to Server!\n")

        # Begin initialization phase

        start_time = time.time()

        for i in range(28):
            data = pickle.dumps(test_key_shares[i])
            client_socket.sendall(data)
            time.sleep(TIME_DELAY)
        time.sleep(TIME_DELAY)
        client_socket.sendall(b"READY")

        print("shares sent\n")

        # Begin cut and choose phase
        # Receive opening key and evaluation key indices

        indices = []
        while True:
            data = client_socket.recv(1024)
            if data.endswith(b"READY"):
                break
            indices += pickle.loads(data)

        if len(indices) != 0:
            print(len(indices), " Indices received\n")
        else: 
            print("Error in initialization phase, aborting protocol\n")

        opening_key_indices = indices[:14]
        eval_key_indices = indices[14:]
        
        print("Indices received from server\n")

        for i in range(14):
            data = pickle.dumps(test_key_shares[opening_key_indices[i]])
            client_socket.sendall(data)
            time.sleep(TIME_DELAY)

        data = b"READY"
        client_socket.sendall(data)

        print("Sent opening key shares to server\n")

        # Begin session key derivation phase
        # Randomly select a secret S

        secret = b"25" # should be random
        ciphers = []

        for i in range(14):
            cipher = AES.new(test_keys[eval_key_indices[i]], AES.MODE_ECB)
            ciphertext = cipher.encrypt(pad(secret, AES.block_size))
            ciphers.append(ciphertext)
            #print("Secret: ", ciphers[i], "\n")

        data = pickle.dumps(ciphers)
        client_socket.sendall(data)

        print("Sent ciphertexts to server\n")

        key = scrypt(secret.decode(), "salt", 16, N=2**10, r=8, p=1) # TODO use random salt

        end_time = time.time() - start_time

        print("Session Key: ", key, " took", end_time, "seconds\n")

        # Start communication with encrypted messages using derived key

        while True:
            user_input = input("Enter your message: ")
            if user_input == "quit":
                print("\nGoodbye!")
                break
            send_encrypted_message(client_socket, key, user_input)

    except Exception as e:
        print("\nError: ", e, "\n")