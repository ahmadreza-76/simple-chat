import socket
import threading

def handle_client(connection, address, clients, usernames):
    # Ask the client for a username
    username = connection.recv(1024).decode().strip()
    print(f"username received: {username}")
    while username in usernames:
        # Ask the client for a different username if it's not unique
        connection.send(b"That username is already taken. Enter a different username: ")
        username = connection.recv(1024).decode().strip()
    usernames.add(username)
    connection.send(b"username succesfull ")
    # Add the client to the clients dictionary using their username as the key
    clients[username] = connection
    # Ask the client who they want to chat with
    target_username = connection.recv(1024).decode().strip()
    print(f"{username}: target username received: {target_username}")
    if target_username in clients:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            message = data.decode()
            clients[target_username].send(f"{username}: {message}".encode())
            print(f"for user {username} from {target_username} message: {message}")
    else:
        clients[username].send(f"Client with username {target_username} not found".encode())

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
s.bind(("localhost", 12345))

# Listen for incoming connections
s.listen(5)

print("Waiting for a connection...")

clients = {}
usernames = set()

while True:
    # Accept a connection
    connection, address = s.accept()
    # Create a new thread for the client
    client_thread = threading.Thread(target=handle_client, args=(connection, address, clients, usernames))
    client_thread.start()

# close the cursor
# close the cursor and the database connection when done.
