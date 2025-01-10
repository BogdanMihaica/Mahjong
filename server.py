import socket
import threading
import pickle
import pygame as pg
import random
# Socket configuration
HOST = "127.0.0.1"
PORT = 65432


#DEMO CARDS
players = [
    [   # Player 1 (15 cards)
        
        # Test win
        # {'character_1': 'tiles/character_1.jpg'},
        # {'character_2': 'tiles/character_2.jpg'},
        # {'character_3': 'tiles/character_3.jpg'},
        # {'stick_7': 'tiles/stick_7.jpg'},
        # {'stick_8': 'tiles/stick_8.jpg'},
        # {'stick_9': 'tiles/stick_9.jpg'},
        # {'dragon_2': 'tiles/dragon_2.jpg'},
        # {'dragon_2': 'tiles/dragon_2.jpg'},
        # {'dragon_2': 'tiles/dragon_2.jpg'},
        # {'dragon_1': 'tiles/dragon_1.jpg'},
        # {'dragon_1': 'tiles/dragon_1.jpg'},
        # {'dragon_1': 'tiles/dragon_1.jpg'},
        # {'wind_1': 'tiles/wind_1.jpg'},
        # {'wind_1': 'tiles/wind_1.jpg'},

        # Test flowers and pick card
        {'wind_3': 'tiles/wind_3.jpg'},
        {'character_6': 'tiles/character_6.jpg'},
        {'character_5': 'tiles/character_5.jpg'},
        {'stick_8': 'tiles/stick_8.jpg'},
        {'season_1': 'tiles/season_1.jpg'},
        {'stick_4': 'tiles/stick_4.jpg'},
        {'dot_6': 'tiles/dot_6.jpg'},
        {'dragon_3': 'tiles/dragon_3.jpg'},
        {'wind_2': 'tiles/wind_2.jpg'},
        {'flower_4': 'tiles/flower_4.jpg'},
        {'dragon_1': 'tiles/dragon_1.jpg'},
        {'flower_2': 'tiles/flower_2.jpg'},
        {'stick_6': 'tiles/stick_6.jpg'},
        {'dot_3': 'tiles/dot_3.jpg'},
     
    ],
    [   # Player 2 (14 cards)
        {'flower_2': 'tiles/flower_2.jpg'},
        {'wind_3': 'tiles/wind_3.jpg'},
        {'stick_3': 'tiles/stick_3.jpg'},
        {'character_4': 'tiles/character_4.jpg'},
        {'character_6': 'tiles/character_6.jpg'},
        {'stick_2': 'tiles/stick_2.jpg'},
        {'season_2': 'tiles/season_2.jpg'},
        {'character_3': 'tiles/character_3.jpg'},
        {'wind_4': 'tiles/wind_4.jpg'},
        {'dragon_3': 'tiles/dragon_3.jpg'},
        {'dot_1': 'tiles/dot_1.jpg'},
        {'stick_5': 'tiles/stick_5.jpg'},
        {'character_2': 'tiles/character_2.jpg'}
    ],
    [   # Player 3 (14 cards)
        {'wind_1': 'tiles/wind_1.jpg'},
        {'dot_4': 'tiles/dot_4.jpg'},
        {'stick_2': 'tiles/stick_2.jpg'},
        {'dot_2': 'tiles/dot_2.jpg'},
        {'character_4': 'tiles/character_4.jpg'},
        {'stick_8': 'tiles/stick_8.jpg'},
        {'season_3': 'tiles/season_3.jpg'},
        {'wind_4': 'tiles/wind_4.jpg'},
        {'character_9': 'tiles/character_9.jpg'},
        {'stick_1': 'tiles/stick_1.jpg'},
        {'flower_1': 'tiles/flower_1.jpg'},
        {'dot_5': 'tiles/dot_5.jpg'},
        {'dragon_1': 'tiles/dragon_1.jpg'}
    ],
    [   # Player 4 (14 cards)
        {'stick_2': 'tiles/stick_2.jpg'},
        {'character_1': 'tiles/character_1.jpg'},
        {'stick_5': 'tiles/stick_5.jpg'},
        {'dot_5': 'tiles/dot_5.jpg'},
        {'dot_1': 'tiles/dot_1.jpg'},
        {'dragon_2': 'tiles/dragon_2.jpg'},
        {'dot_7': 'tiles/dot_7.jpg'},
        {'stick_3': 'tiles/stick_3.jpg'},
        {'flower_4': 'tiles/flower_4.jpg'},
        {'wind_2': 'tiles/wind_2.jpg'},
        {'dragon_3': 'tiles/dragon_3.jpg'},
        {'season_4': 'tiles/season_4.jpg'},
        {'character_3': 'tiles/character_3.jpg'}
    ]
]

# Card defining

all_cards = []
values = {
    # Stick cards: 1–9
    "stick_1": 1, "stick_2": 2, "stick_3": 3, "stick_4": 4, "stick_5": 5,
    "stick_6": 6, "stick_7": 7, "stick_8": 8, "stick_9": 9,
    
    # Dot cards: 20–28
    "dot_1": 20, "dot_2": 21, "dot_3": 22, "dot_4": 23, "dot_5": 24,
    "dot_6": 25, "dot_7": 26, "dot_8": 27, "dot_9": 28,
    
    # Character cards: 40–48
    "character_1": 40, "character_2": 41, "character_3": 42, "character_4": 43,
    "character_5": 44, "character_6": 45, "character_7": 46, "character_8": 47, "character_9": 48,
    
    # Dragon cards: 60–62
    "dragon_1": 60, "dragon_2": 61, "dragon_3": 62,
    
    # Wind cards: 80–83
    "wind_1": 80, "wind_2": 81, "wind_3": 82, "wind_4": 83,
    
    # Flower cards: 100 (all share the same value)
    "flower_1": 100, "flower_2": 100, "flower_3": 100, "flower_4": 100,
    
    # Season cards: 120 (all share the same value)
    "season_1": 120, "season_2": 120, "season_3": 120, "season_4": 120
}


def load_image(path, size):
        try:
            img = pg.image.load(path)
            return pg.transform.scale(img, size)
        except FileNotFoundError:
            print(f"Error: File not found {path}")
            return pg.Surface(size)


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
#players=[player1,player2,player3,player4]
drawable = all_cards[53:]
discarded=[]


# Game state
clientsConnected = 0
game_started = False
lock = threading.Lock()
clients = []  # To store client connections
gameState={
   "status":"ongoing",
   "turn": 0,
   "exposed": [[],[],[],[]],
   "discarded": []
}
  
def broadcast_object(obj):
     """Send an object to all connected clients."""
     for client in clients:
            try:
                ob=pickle.dumps(obj)
                client.sendall(ob)
            except Exception as e:
                print(f"Failed to send object to client: {e}")
def broadcast(message):
    """Send a message to all connected clients."""
    
    for client in clients:
            try:
                client.sendall(message)
            except Exception as e:
                print(f"Failed to send message to client: {e}")





def broadcast_numbers():
    """Send the player index to all connected clients."""
    nums=[b"1",b"2",b"3",b"4"]
    for index,client in enumerate(clients):
            try:
                client.sendall(nums[index])
            except Exception as e:
                print(f"Failed to send player index to client: {e}")

def check_consecutive(arr):
    for i in range(1,len(arr)):
        if arr[i]-arr[i-1]!=1 or arr[i]>62:
            return False
    return True
def check_equal(arr):
    for i in range(1,len(arr)):
        if arr[i]-arr[i-1]!=0 or arr[i]>83:
            return False
    return True
def check_gong(cards,target):
    for i in range(len(cards)-2):
        partition=cards[i:i+3]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        gong=check_equal(newPartition)
        if gong:
            return i
    return -1

def check_pong(cards,target):
    for i in range(len(cards)-1):
        partition=cards[i:i+2]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        pong=check_equal(newPartition)
        if pong:
            return i
    return -1

def check_seung(cards,target):
    for i in range(len(cards)-1):
        partition=cards[i:i+2]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        newPartition.sort()
        seung=check_consecutive(newPartition)
        if seung:
            return i
    return -1
def check_pair(card_1,card_2):
    return values[card_1]-values[card_2]==0

def check_winning(cards):
    for i in range(0,len(cards),3):
        part=cards[i:i+3]
       
        if len(part)==3:
            newPartition = []
            for card in part:
                newPartition.append(values[card])
            newPartition.sort()
            if not (check_consecutive(newPartition) or check_equal(newPartition)):
                return False
        elif len(part)==2:
            if not check_pair(part[0],part[1]):
                return False
    return True

test= [
    "stick_2", "stick_3", "stick_4", 
    "dot_3", "dot_3", "dot_3",        
    "character_5", "character_5", "character_5",  
    "wind_1", "wind_1", "wind_1",
    "stick_1", "stick_1"      
]


def expose_cards(index, player, nr_cards, target):
    global gameState, players
    nr_cards -= 1
    
    to_append = players[player-1][index:index+nr_cards]
    
    to_append.append(target)
    to_append=sorted(to_append, key=lambda x: next(iter(x)))

    
    gameState["exposed"][player-1].extend(to_append)
    
    new_player_cards = players[player-1][:index] + players[player-1][index+nr_cards:]
    players[player-1] = new_player_cards

def send_cards_to_players():
    for index,client in enumerate(clients):
            try:
                cards=pickle.dumps(players[index])
                client.sendall(cards)
            except Exception as e:
                print(f"Failed to send cards to player: {e}")
def send(conn,message):
    toSend=pickle.dumps(message)
    conn.sendall(toSend)


def handle_player(player,conn):
    # Data formats: 
    # {"player": number, "action": "pick", "args": [player_cards]}    - no need to be his turn and the card has to be freshly discarded 
    # {"player": number, "action": "draw", "args": [player_cards]}    - needs to be his turn and the card has to be freshly discarded 
    # {"player": number, "action": "discard", "args": [player_cards,card_index]} - needs to be his turn and the card has to be freshly discarded
                                                                                                                                            
                  
    # If pick action happens, server decides if it is for a gong, pong or seung (in this order)
    # If it is a players turn, if it has flowers, display them and give them the ability to draw again
    # If a player picks a card, check for flowers again
    # If the server decides GONG, give the ability to draw again

    # Response formats:
    
    while True:
        if gameState["turn"]<4:
            found=False
            how_many=0
            index=gameState["turn"]
            for i,card in enumerate(players[index]):
                name=list(card.keys())[0]
                if values[name]>=100:
                    gameState["exposed"][index].append(players[index][i])
                    players[index].pop(i)
                    found=True
                    how_many+=1
            if found:
                message={
                    "type":"flower",
                    "content":[how_many,players[index]]
                }
                send(clients[index],message)
                message={
                    "type":"state",
                    "content":gameState
                }
                broadcast_object(message)
                
               


        try:
            data = conn.recv(1024)
            if data:
                request=pickle.loads(data)
                if request["action"]=="draw":
                    if request["player"]!=gameState["turn"]%4+1:
                        message={
                            "type": "warning",
                            "content":  "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn,message)
                    else:
                        newCard=all_cards.pop()
                        ind=request["player"]-1
                        playerCards=request["args"][0]
                        value=values[list(newCard.keys())[0]]
                        players[ind]=playerCards
                        if value<100:
                            playerCards.append(newCard)
                            players[ind]=playerCards
                            message={
                                "type": "drawn",
                                "content":  players[ind]
                            }
                            send(conn,message)
                        else:
                            gameState["exposed"][ind].append(newCard)
                            message={
                                "type":"flower-draw",
                                "content":[0,players[ind]]
                            }
                            send(conn,message)
                            message={
                                "type":"state",
                                "content":gameState
                            }
                            broadcast_object(message)


                if request["action"]=="pick":
                     
                    if len(discarded)==0:
                        message= {
                            "type": "warning",
                            "content":  "There are no discards"
                        }
                        send(conn,message)
                    else:
                        playerCards=request["args"][0]
                        rawTarget=discarded[-1]
                        target=list(discarded[-1].keys())[0]
                        cards= [list(card.keys())[0] for card in playerCards]
                        players[player-1]=playerCards
                        cards_to_expose=0
                        index=-1
                        #check if a gong can happen
                        gong=check_gong(cards,target)

                        if gong>=0:
                            message={
                                "type": "warning",
                                "content":  "GONG"
                            }
                            send(conn,message)
                            message={
                            "type":"flower",
                            "content":[0,players[index]]
                            }
                            send(clients[index],message)
                            cards_to_expose=4
                            index=gong
                        else:
                            pong=check_pong(cards,target)
                            if pong>=0:
                                message={
                                    "type": "warning",
                                    "content":  "PONG"
                                }
                                send(conn,message)
                                cards_to_expose=3
                                index=pong
                            else:
                                seung=check_seung(cards,target) if request["player"]==gameState["turn"]%4+1 else -1
                                if seung>=0:
                                    message={
                                        "type": "warning",
                                        "content":  "SEUNG"
                                    }
                                    send(conn,message)
                                    cards_to_expose=3
                                    index=seung
                                else:
                                    message={
                                        "type": "warning",
                                        "content":  "No pong/gong/seung"
                                    }
                                    send(conn,message)
                        if index>=0:
                            expose_cards(index,request["player"],cards_to_expose,rawTarget)
                            #discarded.pop()
                            gameState["discarded"].pop()
                            message={
                                "type": "state",
                                "content":  gameState
                            }
                            broadcast_object(message)
                            message={
                                "type": "drawn",
                                "content":  players[request["player"]-1]
                            }
                            send(conn,message)
                            
                    
                if request["action"]=="discard":
                     if request["player"]!=gameState["turn"]%4+1:
                        message={
                            "type": "warning",
                            "content":  "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn,message)
                     else:
                         cardIndex=request["args"][1]
                         playerCards=request["args"][0]
                        
                         player=request["player"]
                         print(playerCards[cardIndex])
                         discarded.append(playerCards[cardIndex])
                         playerCards.pop(cardIndex)
                         players[player-1]=playerCards
                         message={
                            "type": "discarded",
                            "content":  players[player-1]
                         }
                         send(conn,message)
                         gameState["turn"]=gameState["turn"]+1
                         gameState["discarded"]=discarded
                         
                         message= {
                            "type": "state",
                            "content":  gameState
                         }

                         broadcast_object(message)
                if request["action"]=="check":
                    if request["player"]!=gameState["turn"]%4+1:
                        message={
                            "type": "warning",
                            "content":  "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn,message)
                    else:
                        playerCards=request["args"][0]
                        modified=[]
                        for card in playerCards:
                            modified.append(list(card.keys())[0])
                        check=check_winning(modified)
                        if check:
                            message={
                                "type": "win",
                                "content": request["player"]
                            }
                            broadcast_object(message)
                        else:
                            message={
                                "type": "warning",
                                "content": "Not a winning hand!"
                            }
                            send(conn,message)

                         

        except Exception as e:
             print(f"Some exception occured: {e}")



def handle_game():
    """Main game loop to handle player actions."""
    global gameState, clients
    for index, conn in enumerate(clients):
        threading.Thread(target=handle_player, args=(index+1,conn), daemon=True).start()
                  
             


def wait_for_client_responses(expected_clients):
    """Wait for all clients to send their 'ready' response."""
    responses = 0
    while responses < expected_clients:
        for conn in clients:
            try:
                data = conn.recv(1024)
                if data == b"ready":
                    responses += 1
                    print(f"Client {conn} is ready. Total ready: {responses}/{expected_clients}")
            except Exception as e:
                print(f"Error receiving client response: {e}")
    print("All clients are ready.")
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
                    broadcast_numbers() #announces players what is their turn 
                    wait_for_client_responses(4)
                    send_cards_to_players()
                    threading.Thread(target=handle_game, daemon=True).start()
                elif clientsConnected > 4:
                    print("Game is full. No more connections are allowed.")
                    conn.sendall(b"Game is full. No more connections are allowed.")
                    conn.close()


if __name__ == "__main__":
    main()
