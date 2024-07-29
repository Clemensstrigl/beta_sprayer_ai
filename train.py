import socket
import json

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def handle_client(conn, addr):
    """Handles communication with a connected client."""
    print('Connected by', addr)
    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break

        try:
            client_data = json.loads(data)
            print("Client data: ", client_data)

            # Process the client's data and generate a response
            # (Replace this with your simulation logic)
            response_data = {
                "x": client_data.get("x", 0) + 0.2,  # Example: Move the cube 0.1 units in the X direction
                "y": client_data.get("y", 0) + 0.2,
                "z": client_data.get("z", 0) ,
            }

            # Send the response back to the client
            conn.sendall(json.dumps(response_data).encode('utf-8'))
            print("data sent back to client")
        except json.JSONDecodeError:
            print("Error decoding JSON data:", data)

    conn.close()
    print('Connection closed:', addr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Server listening on port', PORT)

    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)