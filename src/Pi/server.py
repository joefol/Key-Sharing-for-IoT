import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Server is listening for connections...")

    conn, addr = server_socket.accept()
    with conn:
        print('Connected by', addr)

        # Start pi
        