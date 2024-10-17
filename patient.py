import ssl
import socket
import random
import time

def connect_to_Hospital(patient_name, cert_file, key_file):
    # Create a client socket needed to connect to the hospital.
    client_socket = socket.create_connection(('127.0.0.1', 12345)) 

    # Create context and load own certificate as well as hospital cert
    context = ssl.create_default_context()
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    context.load_verify_locations('certs/hospital_cert.pem') 

    with context.wrap_socket(client_socket, server_hostname='Hospital') as tls_sock:
        print(f"{patient_name} connected to Hospital.")

        # Send a message to Hospital
        message = f"Hello from {patient_name}!"
        message_bytes = message.encode('utf-8')

        try:
            tls_sock.sendall(message_bytes)
            print(f"Message sent to Hospital from {patient_name}")
            
            # This seems to be necessary to have. Without it, there are some instances where if multiple patients connects and send messages,
            # the messages don't go through properly? I think by using the recv function we wait for a confirmation from the server socket
            # before continuing.
            response = tls_sock.recv(1024) 
            print(f"Received from Hospital ack from hospital, closing ...")
        except Exception as e:
            print(f"Error: {e}")
  
    client_socket.close()
    print(f"{patient_name} connection closed. \n")


def listen_for_other_patients(patient_name, cert_file, key_file, port, trusted_certs):
    # Creating a server socket for the patient to listen for connections, so they basically act as the hospital does.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

    # Load the patients own certificate.
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    # Load the certificates of other patients
    for cert in trusted_certs:
        context.load_verify_locations(cert)

    print(f"{patient_name} is listening on port {port}\n")

    while True:

        client, addr = server_socket.accept()
        with context.wrap_socket(client, server_side=True) as tls_socket:
            print(f"Connection with {addr}")

            data = tls_socket.recv(1024)
            print(f"Message received: {data.decode('utf-8')}")
            client.close()


def connect_to_other_patients(patient_name, cert_file, key_file, patient_secret, other_patients):
    context = ssl.create_default_context()
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    # Sample n-1 random shares
    s1 = random.randint(0, 100)
    s2 = random.randint(0, 100)
    s3 = patient_secret - (s1 + s2)
    

    # Connect and send shares to other patients
    for other_patient, port, cert in other_patients:
        client_socket = socket.create_connection(('127.0.0.1', port))
        context.load_verify_locations(cert)

        with context.wrap_socket(client_socket, server_hostname=other_patient) as tls_sock:
            print(f"{patient_name} connected to {other_patient}.")

            # Determine which share to send
            if other_patient == 'bob':
                message = f"From {patient_name}, S1 = {s1}"
            elif other_patient == 'charlie':
                message = f"From {patient_name}, S2 = {s2}"

            tls_sock.send(message.encode('utf-8'))
            print(f"Sent message to {other_patient}")
        client_socket.close()

def start_patient(patient_name):
    cert_file = f'certs/{patient_name}_cert.pem'
    key_file = f'certs/{patient_name}_key.pem'
    patient_secret = 40 

    trusted_certs = ['certs/bob_cert.pem', 'certs/charlie_cert.pem', 'certs/alice_cert.pem']
    other_patients = [('bob', 12348, 'certs/bob_cert.pem'), ('charlie', 12346, 'certs/charlie_cert.pem'), ('alice', 12347, 'certs/alice_cert.pem')]

    #listen_for_other_patients(patient_name, cert_file, key_file, 12347, trusted_certs)
    #connect_to_other_patients(patient_name, cert_file, key_file, patient_secret, other_patients) 
    connect_to_Hospital(patient_name, cert_file, key_file)


if __name__ == "__main__":
    patients = ['charlie','bob','alice']
    
    for p in patients:
        print(f"\nTrying patient {p} ...")
        start_patient(p)
        time.sleep(2)
