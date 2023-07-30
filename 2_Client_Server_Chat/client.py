import socket
import threading

def receive_messages(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("Received:", data)

def start_client():
    host = "127.0.0.1"  # Localhost
    port = 12345       # The same port number as in the server script

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    print("You can start the chat")

    while True:
        message = input()
        client_socket.sendall(message.encode())
        if message.lower() == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
