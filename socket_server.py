import socket
import json
from datetime import datetime
from pymongo import MongoClient

def save_message_to_db(message_data):
    client = MongoClient('mongodb://mongo:27017/')  # Use 'mongo' as the hostname
    db = client.message_db
    messages = db.messages
    message_data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    messages.insert_one(message_data)

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5001))  # Bind to all interfaces
    server_socket.listen(5)
    print('Socket server started on port 5001')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr} has been established!')
        data = client_socket.recv(1024).decode('utf-8')
        message_data = json.loads(data)
        save_message_to_db(message_data)
        client_socket.close()

if __name__ == "__main__":
    start_socket_server()