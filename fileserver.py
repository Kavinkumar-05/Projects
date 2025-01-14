import socket


def handle_client_connection(client_socket):
    # Open a file to save the received data
    with open("received_file.txt", "wb") as file:
        print("Receiving file...")
        while True:
            # Receive data from the client in chunks
            data = client_socket.recv(1024)
            if not data:
                break  # Break when there is no more data
            file.write(data)  # Write data to the file
        print("File received successfully!")

    client_socket.close()


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the server to an IP and port
    server_socket.bind(("127.0.0.1", 55555))

    # Listen for incoming client connections
    server_socket.listen(1)
    print("Server is waiting for a connection...")

    while True:
        # Accept the client connection
        client_socket, addr = server_socket.accept()
        print(f"Connected to {addr}")

        # Handle the file transfer in a separate function
        handle_client_connection(client_socket)


if __name__ == "__main__":
    start_server()
