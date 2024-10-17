import ssl
import socket

def start_server():
    # Creating a socket for Hospital
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))  # Hospital listens on port 12345
    server_socket.listen(5)

    # Load own certificate and private key
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='certs/hospital_cert.pem', keyfile='certs/hospital_key.pem')


    #Add certificates of patients so that they can connect
    context.load_verify_locations('certs/alice_cert.pem') 
    context.load_verify_locations('certs/bob_cert.pem') 
    context.load_verify_locations('certs/charlie_cert.pem') 


    print("Hospital is listening for connections...")
    counter = 0
    while True:
        # Accept an incoming connection
        client, addr = server_socket.accept()
        with context.wrap_socket(client, server_side=True) as tls_socket:
            print(f"Connection established with {addr}")

            # Receive and print the patient's message
            try:
                data = tls_socket.recv(2048)  # Blocking call, waits for incoming data
                if data:
                    print(f"Received data: {data.decode('utf-8')}")
                else:
                    print("Received empty message")

            except Exception as e:
                print(f"Error receiving data: {e}")
            
            client.close()  # Close the connection
            counter += 1
            print("Counter: ", counter)

            # Exit after receiving 3 messages
            if counter == 3:
                print("All patient data received, exiting...")
                break

start_server()
