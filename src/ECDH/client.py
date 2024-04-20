import socket
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Hash import SHAKE128
import time

# Client Configuration
HOST = '127.0.0.1'
PORT = 65432

def kdf(x):
        return SHAKE128.new(x).read(32)

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    start_time = time.time()

    # Generate client's private key and public key
    client_key = ECC.generate(curve='secp256r1')
    client_public_key = client_key.public_key().export_key(format='SEC1')

    # Send client's public key to server
    client_socket.sendall(client_public_key)

    # Receive server's public key
    server_public_key_bytes = client_socket.recv(2048)
    server_public_key = ECC.import_key(server_public_key_bytes, curve_name='secp256r1')

    # Perform key agreement
    client_key_agreement = key_agreement(static_priv=client_key, static_pub=server_public_key, kdf=kdf)
    shared_key = PBKDF2(client_key_agreement, b'salt', 16, count=1000000)

    end_time = time.time() - start_time

    # Print shared key
    print("Client's shared key:", shared_key.hex())
    print("\nTime to derive session key using ECDH: ", end_time, "\n")