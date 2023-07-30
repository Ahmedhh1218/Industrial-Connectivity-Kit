import socket

def start_server():
    host = "127.0.0.1"  # Localhost
    port = 12345       # Arbitrary port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server is waiting for connections...")

    conn, addr = server_socket.accept()
    print("Connected by:", addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("Received:", data)

    conn.close()

if __name__ == "__main__":
    start_server()
