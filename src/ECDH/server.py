import socket
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Hash import SHAKE128

# Server Configuration
HOST = '127.0.0.1'
PORT = 65432

def kdf(x):
        return SHAKE128.new(x).read(32)

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is listening for connections...")

    # Accept connection
    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)

        # Generate server's private key and public key
        server_key = ECC.generate(curve='secp256r1')
        server_public_key = server_key.public_key().export_key(format='SEC1')

        # Send server's public key to client
        conn.sendall(server_public_key)

        # Receive client's public key
        client_public_key_bytes = conn.recv(2048)
        client_public_key = ECC.import_key(client_public_key_bytes, curve_name='secp256r1')

        # Perform key agreement
        server_key_agreement = key_agreement(static_priv=server_key, static_pub=client_public_key, kdf=kdf)
        shared_key = PBKDF2(server_key_agreement, b'salt', 16, count=1000000)

        # Print shared key
        print("Server's shared key:", shared_key.hex())