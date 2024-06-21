import socket
import select

# Configuration
HOST = '83.136.255.100'  # The server's hostname or IP address
PORT = 45887  # The port used by the server

def handle_response(message):
    """
    Determines the response based on the message content.
    """
    response_parts = []
    if 'GEORGE' in message:
        response_parts.append('STOP')
    if 'PHREAK' in message:
        response_parts.append('DROP')
    if 'FIRE' in message:
        response_parts.append('ROLL')
    
    return '-'.join(response_parts) if response_parts else 'No action'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to the server.")
    
    # Flag to identify the first interaction
    first_interaction = True

    while True:
        ready_to_read, _, _ = select.select([s], [], [], 1)
        if ready_to_read:
            data = s.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            
            message = data.decode('utf-8').strip()
            print(f"Received: {message}")

            # For the first message received, just respond with 'y'
            if first_interaction:
                s.sendall(b'y')
                print("Sent: 'y'")
                first_interaction = False
            else:
                response = handle_response(message)
                if response != 'No action':
                    s.sendall(response.encode('utf-8'))
                    print(f"Sent: {response}")
        else:
            # No data received, server may not have sent anything yet.
            print("Waiting for data from the server...")
