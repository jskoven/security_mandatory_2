import ssl
import socket

def connect_to_hospital():
    # Create a socket for Alices client
    client_socket = socket.create_connection(('127.0.0.1', 12345))  # Connect to Alices server

    # Load Alices certificate and private key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/alice_cert.pem', keyfile='certs/alice_key.pem')
    context.load_verify_locations('certs/hospital_cert.pem')  # Trust Hospital certificate

    with context.wrap_socket(client_socket, server_hostname='hospital') as tls_sock:
        print("Alice connected to hospital")

        # Send a message to Alice
        while True:
            message = "Hello from Alice"
            message_bytes = message.encode('utf-8')
            tls_sock.send(message_bytes)
            exit()

connect_to_hospital()

