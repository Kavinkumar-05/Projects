import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 2121
BUFFER_SIZE = 1024

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f"[INFO] Connected to FTP server at {SERVER_HOST}:{SERVER_PORT}")

    while True:
        command = input("Enter command (LIST, UPLOAD <filename>, DOWNLOAD <filename>, QUIT): ").strip()
        client_socket.send(command.encode())

        if command == "LIST":
            response = client_socket.recv(BUFFER_SIZE).decode()
            print("Server Files:\n" + response)

        elif command.startswith("UPLOAD"):
            _, filename = command.split(" ", 1)
            try:
                with open(filename, "rb") as f:
                    while chunk := f.read(BUFFER_SIZE):
                        client_socket.send(chunk)
                client_socket.send(b"END")
                print(client_socket.recv(BUFFER_SIZE).decode())
            except FileNotFoundError:
                print(f"[ERROR] File {filename} not found.")

        elif command.startswith("DOWNLOAD"):
            _, filename = command.split(" ", 1)
            with open(f"downloaded_{filename}", "wb") as f:
                while True:
                    data = client_socket.recv(BUFFER_SIZE)
                    if data == b"END":
                        break
                    f.write(data)
            print(f"[SUCCESS] Downloaded {filename}")

        elif command == "QUIT":
            print(client_socket.recv(BUFFER_SIZE).decode())
            break

        else:
            print(client_socket.recv(BUFFER_SIZE).decode())

    client_socket.close()

if __name__ == "__main__":
    start_client()