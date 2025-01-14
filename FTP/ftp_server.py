import socket
import os
from threading import Thread

HOST = '0.0.0.0'
PORT = 2121
BUFFER_SIZE = 1024

def handle_client(client_socket, client_address):
    print(f"[INFO] Connection established with {client_address}")
    while True:
        try:
            command = client_socket.recv(BUFFER_SIZE).decode().strip()
            if not command:
                break

            if command == "LIST":
                files = os.listdir()
                client_socket.send("\n".join(files).encode())
            elif command.startswith("UPLOAD"):
                _, filename = command.split(" ", 1)
                with open(filename, "wb") as f:
                    while True:
                        data = client_socket.recv(BUFFER_SIZE)
                        if data == b"END":
                            break
                        f.write(data)
                client_socket.send(f"[SUCCESS] Uploaded {filename}".encode())

            elif command.startswith("DOWNLOAD"):
                _, filename = command.split(" ", 1)
                if os.path.exists(filename):
                    with open(filename, "rb") as f:
                        while chunk := f.read(BUFFER_SIZE):
                            client_socket.send(chunk)
                    client_socket.send(b"END")
                else:
                    client_socket.send(f"[ERROR] File {filename} not found.".encode())

            elif command == "QUIT":
                client_socket.send(b"Goodbye!")
                break

            else:
                client_socket.send(b"[ERROR] Invalid command.")
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"[INFO] Connection closed with {client_address}")
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[INFO] FTP server running on {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    start_server()