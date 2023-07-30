import socket
import threading

def handle_client(conn, addr):
    print(f"Connected by: {addr[0]}:{addr[1]}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received from {addr[0]}:{addr[1]}: {data}")
            response = input("Enter a response to send: ")
            conn.sendall(response.encode())
    except Exception as e:
        print(f"Error with {addr[0]}:{addr[1]}:", e)
    finally:
        conn.close()
        print(f"Connection closed by: {addr[0]}:{addr[1]}")

def start_server():
    host = "127.0.0.1"  # Localhost
    port = 12345       # Arbitrary port number

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
