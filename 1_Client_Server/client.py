import socket

def start_client():
    host = "127.0.0.1"  # Localhost
    port = 12345       # The same port number as in the server script

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        message = input("Enter a message to send (type 'exit' to quit): ")
        client_socket.sendall(message.encode())
        if message.lower() == "exit":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
