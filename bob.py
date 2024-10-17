import ssl
import socket
import random

def connect_to_Hospital():
    # Create a socket for Charlie's client
    client_socket = socket.create_connection(('127.0.0.1', 12345))  # Connect to Hospital's server

    # Load Charlie's certificate and private key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/charlie_cert.pem', keyfile='certs/charlie_key.pem')
    context.load_verify_locations('certs/hospital_cert.pem')  # Trust hospital certificate

    with context.wrap_socket(client_socket, server_hostname='Hospital') as tls_sock:
        print("Bob connected to Hospital.")

        # Send a message to Hospital
        message = "Hello from Bob!"
        message_bytes = message.encode('utf-8')

        try:
            tls_sock.sendall(message_bytes)  # Send all the data at once
            print("Message sent to Hospital")
            
            # Wait for server confirmation (optional step)
            response = tls_sock.recv(1024)  # Wait for acknowledgment from the server
            print(f"Received from Hospital: {response.decode('utf-8')}")
        except Exception as e:
            print(f"Error during communication: {e}")
    
    # Explicitly close the socket after sending the message
    client_socket.close()
    print("Connection closed.")
def listen_for_other_patients():
    # Creating a socket for Bob, so that the other two patients can connect and send
    # messages to Bob.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12348))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    #Load own certification so others will recognize him
    context.load_cert_chain(certfile='certs/bob_cert.pem', keyfile='certs/bob_key.pem')

    #Load other patient certs so we trust them
    context.load_verify_locations('certs/alice_cert.pem') 
    context.load_verify_locations('certs/charlie_cert.pem')

    print("Bob is listening for the other patients")

    while True:
        # Accept an incoming connection
        client, addr = server_socket.accept()
        with context.wrap_socket(client, server_side=True) as tls_socket:
            print(f"Connection established with {addr}")

            # Receive and print Bob's message
            data = tls_socket.recv(1024)
            print(f"Message: {data.decode('utf-8')}")
            client.close()


def connect_to_other_patients():
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/bob_cert.pem', keyfile='certs/bob_key.pem')
    context.load_verify_locations('certs/alice_cert.pem')
    context.load_verify_locations('certs/charlie_cert.pem')

    bob_secret = 60  # Example secret for Bob
    # Sample n-1 random shares
    s1 = random.randint(0, 100)
    s2 = random.randint(0, 100)
    # Compute Sn = S - (s1 + s2)
    s3 = bob_secret - (s1 + s2)
    assert s1 + s2 + s3 == bob_secret, "The sum of shares does not match the secret!"
    
    # Connect and send s1 to Alice
    client_socket = socket.create_connection(('127.0.0.1', 12347)) 
    with context.wrap_socket(client_socket, server_hostname="alice") as tls_sock:

        print(f"Bob connected to Alice.")

        message = f"From Bob, S1 = {s1}"
        tls_sock.send(message.encode('utf-8'))
        print(f"Sent message to Alice")
    
    # Connect and send s2 to Charlie
    client_socket = socket.create_connection(('127.0.0.1', 12346)) 
    with context.wrap_socket(client_socket, server_hostname="charlie") as tls_sock:

        print(f"Bob connected to Charlie.")

        message = f"From Bob, S2 = {s2}"
        tls_sock.send(message.encode('utf-8'))
        print(f"Sent message to Charlie")

#listen_for_other_patients()
connect_to_Hospital()