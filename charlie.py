import ssl
import socket
import random
import time

def connect_to_Hospital():
    # Create a socket for Charlie's client
    client_socket = socket.create_connection(('127.0.0.1', 12345))  # Connect to Hospital's server

    # Load Charlie's certificate and private key
    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/charlie_cert.pem', keyfile='certs/charlie_key.pem')
    context.load_verify_locations('certs/hospital_cert.pem')  # Trust hospital certificate

    with context.wrap_socket(client_socket, server_hostname='Hospital') as tls_sock:
        print("Charlie connected to Hospital.")

        # Send a message to Hospital
        message = "Hello from Charlie!"
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
    # Creating a socket for Charlie, so that the other two patients can connect and send
    # messages to charlie.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12346))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    #Load own certification so others will recognize him
    context.load_cert_chain(certfile='certs/charlie_cert.pem', keyfile='certs/charlie_key.pem')

    #Load other patient certs so we trust them
    context.load_verify_locations('certs/alice_cert.pem') 
    context.load_verify_locations('certs/bob_cert.pem')

    print("Charlie is listening for the other patients")

    while True:
        client_socket, addr = server_socket.accept()
        with context.wrap_socket(client_socket, server_side=True) as tls_sock:
            print(f"Connection established with {addr}")

            data = tls_sock.recv(1024)
            print(f"Message: {data.decode('utf-8')}")
            client_socket.close()

def connect_to_other_patients():

    context = ssl.create_default_context()
    context.load_cert_chain(certfile='certs/charlie_cert.pem', keyfile='certs/charlie_key.pem')
    context.load_verify_locations('certs/alice_cert.pem') 
    context.load_verify_locations('certs/bob_cert.pem')


    charlie_secret = 50
    #Sample n-1 random shares
    s1 = random.randint(0, 100)
    s2 = random.randint(0, 100)
    #Compute Sn = S-(s1+...+sn_1)
    s3 = charlie_secret - (s1 + s2)
    print(f"Found all s values, s1={s1}, s2={s2}, s3={s3}")
    #assert s1 + s2 + s3 == charlie_secret, "The sum of shares does not match the secret!"
    time.sleep(5)

    #connect and send s1 to alice
    client_socket = socket.create_connection(('127.0.0.1', 12347)) 
    with context.wrap_socket(client_socket, server_hostname="alice") as tls_sock:

        print(f"Charlie connected to alice.")

        message = f"From charlie, S1 = {s1}"
        tls_sock.send(message.encode('utf-8'))
        print(f"Sent message to alice")
    #Connect and send s2 to bob
    client_socket = socket.create_connection(('127.0.0.1', 12348)) 
    with context.wrap_socket(client_socket, server_hostname="bob") as tls_sock:

        print(f"Charlie connected to bob.")
        message = f"From charlie, S2 = {s2}"
        tls_sock.send(message.encode('utf-8'))
        print(f"Sent message to bob")
    
#connect_to_other_patients()
connect_to_Hospital()