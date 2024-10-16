import ssl
import socket

def connect_to_alice():
    # Create a socket for Bobs client
    client_socket = socket.create_connection(('127.0.0.1', 12345))  # Connect to Alices server

    # Load Bobs certificate and private key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/bob_cert.pem', keyfile='certs/bob_key.pem')
    context.load_verify_locations('certs/hospital_cert.pem')  # Trust Alices certificate

    with context.wrap_socket(client_socket, server_hostname='Hospital') as tls_sock:
        print("Bob connected to Alice.")

        # Send a message to Alice
        while True:
            message = "Hello from Bob"
            message_bytes = message.encode('utf-8')
            tls_sock.send(message_bytes)
            exit()

connect_to_alice()
