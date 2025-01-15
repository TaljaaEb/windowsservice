import socket
import threading
import rsa
import pickle
import queue

# Server class
class Server:
    def __init__(self, host='0.0.0.0', port=8443):
        self.host = host
        self.port = port
        self.clients = {}  # Mapping of clients and their RSA public keys
        self.pairings = {}  # Mapping of paired clients (client_id -> recipient_id)
        self.client_queues = {}  # Queues for each client to handle incoming messages

        # Generate the server's RSA key pair
        self.server_public_key, self.server_private_key = rsa.newkeys(512)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        print(f"Server started on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        client_id = client_address[1]  # Using port as client identifier
        print(f"Client {client_id} connected from {client_address}")
        
        # Step 1: Send the server's public key to the client
        client_socket.send(pickle.dumps(self.server_public_key))

        # Step 2: Receive the client's public key
        client_public_key = pickle.loads(client_socket.recv(4096))
        self.clients[client_id] = client_public_key
        
        # Step 3: Pairing logic
        self.client_queues[client_id] = queue.Queue()

        while True:
            try:
                # Step 4: Receive a message from the client
                encrypted_message = client_socket.recv(4096)
                if not encrypted_message:
                    break
                
                # Step 5: Decrypt the message using the server's private key
                decrypted_message = rsa.decrypt(encrypted_message, self.server_private_key).decode('utf-8')
                print(f"Received from client {client_id}: {decrypted_message}")

                # Step 6: Forward the message to the intended recipient
                if client_id in self.pairings:
                    recipient_id = self.pairings[client_id]
                    if recipient_id in self.client_queues:
                        self.client_queues[recipient_id].put(decrypted_message)
                else:
                    client_socket.send("No recipient paired.".encode())

            except Exception as e:
                print(f"Error with client {client_id}: {e}")
#                print(encrypted_message)
                break

        print(f"Client {client_id} disconnected.")
        client_socket.close()

    def pair_clients(self, client_id, recipient_id):
        if recipient_id in self.clients:
            self.pairings[client_id] = recipient_id
            print(f"Client {client_id} paired with {recipient_id}")
        else:
            print(f"Recipient client {recipient_id} not found.")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

# Instantiate and start the server
server = Server()
server_thread = threading.Thread(target=server.start)
server_thread.start()
