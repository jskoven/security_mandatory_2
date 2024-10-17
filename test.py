import threading
import time
import charlie  # Import Charlie's functions
import alice    # Import Alice's functions
import bob      # Import Bob's functions

# Threading for Alice, Bob, and Charlie to run concurrently
def start_alice():
    print("Starting alice")
    alice.listen_for_other_patients()  # Alice waits for Charlie's share

def start_bob():
    print("Starting bob")
    bob.listen_for_other_patients()    # Bob waits for Charlie's share

def start_charlie():
    print("Start charlie")
    #time.sleep(10)  # Small delay to ensure Alice and Bob are ready
    charlie.connect_to_other_patients()  # Charlie generates shares and sends them

def main():
    # Step 1: Run Alice and Bob as servers to receive shares from Charlie
    alice_thread = threading.Thread(target=start_alice)
    bob_thread = threading.Thread(target=start_bob)
    
    alice_thread.start()
    bob_thread.start()

    # Step 2: Run Charlie to generate and send shares to Alice and Bob
    charlie_thread = threading.Thread(target=start_charlie)
    charlie_thread.start()

    # Wait for all threads to finish
    alice_thread.join()
    bob_thread.join()
    charlie_thread.join()

    print("Shares have been successfully exchanged between Charlie, Alice, and Bob.")

if __name__ == "__main__":
    main()
