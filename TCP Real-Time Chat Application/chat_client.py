import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICK":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def send_messages():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
send_thread = threading.Thread(target=send_messages)
send_thread.start()