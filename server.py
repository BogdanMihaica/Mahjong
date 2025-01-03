import socket
import threading
import pickle
import pygame as pg
import random
# Socket configuration
HOST = "127.0.0.1"
PORT = 65432



# Card defining
all_cards = []
values = {
        "stick_1": 1, "stick_2": 2, "stick_3": 3, "stick_4": 4, "stick_5": 5, "stick_6": 6, "stick_7": 7, "stick_8": 8, "stick_9": 9,
        "dot_1": 10, "dot_2": 11, "dot_3": 12, "dot_4": 13, "dot_5": 14, "dot_6": 15, "dot_7": 16, "dot_8": 17, "dot_9": 18,
        "character_1": 19, "character_2": 20, "character_3": 21, "character_4": 22, "character_5": 23, "character_6": 24, "character_7": 25, "character_8": 26, "character_9": 27,
        "dragon_1": 28, "dragon_2": 29, "dragon_3": 30,
        "wind_1": 32, "wind_2": 33, "wind_3": 34, "wind_4": 35,
        "flower_1": 36, "flower_2": 36, "flower_3": 36, "flower_4": 36,
        "season_1": 36, "season_2": 36, "season_3": 36, "season_4": 36
}
def load_image(path, size):
        try:
            img = pg.image.load(path)
            return pg.transform.scale(img, size)
        except FileNotFoundError:
            print(f"Error: File not found {path}")
            return pg.Surface(size)

tile_size = (36, 50)
pieces = {
        "stick": {f"stick_{i}":f"tiles/stick_{i}.jpg" for i in range(1, 10)},
        "character": {f"character_{i}": f"tiles/character_{i}.jpg" for i in range(1, 10)},
        "dot": {f"dot_{i}": f"tiles/dot_{i}.jpg" for i in range(1, 10)},
        "wind": {f"wind_{i}": f"tiles/wind_{i}.jpg" for i in range(1, 5)},
        "dragon": {f"dragon_{i}": f"tiles/dragon_{i}.jpg" for i in range(1, 4)},
        "flower": {f"flower_{i}":f"tiles/flower_{i}.jpg" for i in range(1, 5)},
        "season": {f"season_{i}": f"tiles/season_{i}.jpg" for i in range(1, 5)},
    }
for key in pieces:
    iterations = 4
    if key in ["flower", "season"]:
        iterations = 2
    for _ in range(iterations):
        for key1 in pieces[key]:
            all_cards.append({key1: pieces[key][key1]})
random.shuffle(all_cards)
player1 = all_cards[0:14]
player2 = all_cards[14:27]
player3 = all_cards[27:40]
player4 = all_cards[40:53]
players=[player1,player2,player3,player4]
drawable = all_cards[53:]
discarded=[]


# Game state
clientsConnected = 0
game_started = False
lock = threading.Lock()
clients = []  # To store client connections
game_state = {
    "turns": 0,
    "turn": 1,
}

def broadcast(message):
    """Send a message to all connected clients."""
    
    for client in clients:
            print(client)
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Failed to send message to client: {e}")

def send_cards_to_players():
    for index,client in enumerate(clients):
            print(client)
            try:
                cards=pickle.dumps(players[index])
                client.sendall(cards)
            except Exception as e:
                print(f"Failed to send message to client: {e}")
def handle_all_clients():
    """Wait for 4 clients to connect and then broadcast messages to all clients."""
    global game_state, game_started,clients
    
    while True:
        for conn in clients:
            try:
                data = conn.recv(1024)
                if data:
                    pass #aici voi implementa logica
            except ConnectionResetError:
                continue

def main():
    global clientsConnected
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        # Start the client handler thread which will start processing clients once 4 clients are connected
       
        while True:
            conn, addr = s.accept()
            with lock:
                clientsConnected += 1
                clients.append(conn)
                print(f"Connected by {addr}")

                if clientsConnected == 4:
                    print("4 clients connected. The game is starting.")
                    broadcast(b"started")
                    
                    print("All players accepted")
                    #send_cards_to_players()
                    threading.Thread(target=handle_all_clients, daemon=True).start()
                elif clientsConnected > 4:
                    print("Game is full. No more connections are allowed.")
                    conn.sendall(b"Game is full. No more connections are allowed.")
                    conn.close()


if __name__ == "__main__":
    main()
