import socket
import threading

# Socket configuration
HOST = "127.0.0.1"
PORT = 65432

# Game state
clientsConnected = 0
game_started = False
lock = threading.Lock()
clients = []

def handle_client(conn, addr):
    """Function to handle each client's connection."""
    global clientsConnected, game_started
    with conn:
        with lock:
            clientsConnected += 1
            clients.append(conn)
            print(f"Connected by {addr}")
            if clientsConnected == 4 and not game_started:
                game_started = True
                print("Game Started")

        if game_started:
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received from {addr}: {data.decode()}")
                    # Echo back for demonstration (or game-specific logic)
                    conn.sendall(data)
                except ConnectionResetError:
                    break
        with lock:
            clientsConnected -= 1
            clients.remove(conn)
            print(f"Disconnected: {addr}")

def main():
    global game_started
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            if game_started:
                print("Game is ongoing; new connections are not accepted.")
                conn.close()
            else:
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
