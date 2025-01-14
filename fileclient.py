import socket


def send_file(filename, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, server_port))
    print(f"Connected to server at {server_ip}:{server_port}")

    with open(filename, "rb") as file:
        print(f"Sending {filename}...")
        while chunk := file.read(1024):
            client_socket.send(chunk)  # Send the data in chunks
        print("File sent successfully!")

    client_socket.close()


def main():

    filename = input("Enter the file path to send: ")
    server_ip = "127.0.0.1"
    server_port = 55555
    send_file(filename, server_ip, server_port)


if __name__ == "__main__":
    main()
