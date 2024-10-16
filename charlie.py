import ssl
import socket

def connect_to_alice():
    # Creating a socket for Charlie, so that the other two patients can connect and send
    # messages to charlie.
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.bind(('127.0.0.1', 12345))  # Hospital listens on port 12345
    #server_socket.listen(5)



    # Create a socket for Bobs client
    client_socket = socket.create_connection(('127.0.0.1', 12345))  # Connect to Alices server

    # Load Bobs certificate and private key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/charlie_cert.pem', keyfile='certs/charlie_key.pem')
    context.load_verify_locations('certs/hospital_cert.pem')  # Trust Alices certificate

    with context.wrap_socket(client_socket, server_hostname='Hospital') as tls_sock:
        print("Charlie connected to Alice.")

        # Send a message to Alice
        while True:
            message = "Hello from Charlie!"
            message_bytes = message.encode('utf-8')
            tls_sock.send(message_bytes)
            exit()


        
connect_to_alice()
