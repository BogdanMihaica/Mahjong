import socket
import threading
import pickle
import pygame as pg
import random
# Socket configuration
HOST = "127.0.0.1"
PORT = 65432


# DEMO CARDS
# players = [
#     [   # Player 1 (15 cards)

#         # Test win
#         # {'character_1': 'tiles/character_1.jpg'},
#         # {'character_2': 'tiles/character_2.jpg'},
#         # {'character_3': 'tiles/character_3.jpg'},
#         # {'stick_7': 'tiles/stick_7.jpg'},
#         # {'stick_8': 'tiles/stick_8.jpg'},
#         # {'stick_9': 'tiles/stick_9.jpg'},
#         # {'dragon_2': 'tiles/dragon_2.jpg'},
#         # {'dragon_2': 'tiles/dragon_2.jpg'},
#         # {'dragon_2': 'tiles/dragon_2.jpg'},
#         # {'dragon_1': 'tiles/dragon_1.jpg'},
#         # {'dragon_1': 'tiles/dragon_1.jpg'},
#         # {'dragon_1': 'tiles/dragon_1.jpg'},
#         # {'wind_1': 'tiles/wind_1.jpg'},
#         # {'wind_1': 'tiles/wind_1.jpg'},

#         # Test flowers and pick card
#         {'wind_3': 'tiles/wind_3.jpg'},
#         {'character_6': 'tiles/character_6.jpg'},
#         {'character_5': 'tiles/character_5.jpg'},
#         {'stick_8': 'tiles/stick_8.jpg'},
#         {'season_1': 'tiles/season_1.jpg'},
#         {'stick_4': 'tiles/stick_4.jpg'},
#         {'dot_6': 'tiles/dot_6.jpg'},
#         {'dragon_3': 'tiles/dragon_3.jpg'},
#         {'wind_2': 'tiles/wind_2.jpg'},
#         {'flower_4': 'tiles/flower_4.jpg'},
#         {'dragon_1': 'tiles/dragon_1.jpg'},
#         {'flower_2': 'tiles/flower_2.jpg'},
#         {'stick_6': 'tiles/stick_6.jpg'},
#         {'dot_3': 'tiles/dot_3.jpg'},

#     ],
#     [   # Player 2 (14 cards)
#         {'flower_2': 'tiles/flower_2.jpg'},
#         {'wind_3': 'tiles/wind_3.jpg'},
#         {'stick_3': 'tiles/stick_3.jpg'},
#         {'character_4': 'tiles/character_4.jpg'},
#         {'character_6': 'tiles/character_6.jpg'},
#         {'stick_2': 'tiles/stick_2.jpg'},
#         {'season_2': 'tiles/season_2.jpg'},
#         {'character_3': 'tiles/character_3.jpg'},
#         {'wind_4': 'tiles/wind_4.jpg'},
#         {'dragon_3': 'tiles/dragon_3.jpg'},
#         {'dot_1': 'tiles/dot_1.jpg'},
#         {'stick_5': 'tiles/stick_5.jpg'},
#         {'character_2': 'tiles/character_2.jpg'}
#     ],
#     [   # Player 3 (14 cards)
#         {'wind_1': 'tiles/wind_1.jpg'},
#         {'dot_4': 'tiles/dot_4.jpg'},
#         {'stick_2': 'tiles/stick_2.jpg'},
#         {'dot_2': 'tiles/dot_2.jpg'},
#         {'character_4': 'tiles/character_4.jpg'},
#         {'stick_8': 'tiles/stick_8.jpg'},
#         {'season_3': 'tiles/season_3.jpg'},
#         {'wind_4': 'tiles/wind_4.jpg'},
#         {'character_9': 'tiles/character_9.jpg'},
#         {'stick_1': 'tiles/stick_1.jpg'},
#         {'flower_1': 'tiles/flower_1.jpg'},
#         {'dot_5': 'tiles/dot_5.jpg'},
#         {'dragon_1': 'tiles/dragon_1.jpg'}
#     ],
#     [   # Player 4 (14 cards)
#         {'stick_2': 'tiles/stick_2.jpg'},
#         {'character_1': 'tiles/character_1.jpg'},
#         {'stick_5': 'tiles/stick_5.jpg'},
#         {'dot_5': 'tiles/dot_5.jpg'},
#         {'dot_1': 'tiles/dot_1.jpg'},
#         {'dragon_2': 'tiles/dragon_2.jpg'},
#         {'dot_7': 'tiles/dot_7.jpg'},
#         {'stick_3': 'tiles/stick_3.jpg'},
#         {'flower_4': 'tiles/flower_4.jpg'},
#         {'wind_2': 'tiles/wind_2.jpg'},
#         {'dragon_3': 'tiles/dragon_3.jpg'},
#         {'season_4': 'tiles/season_4.jpg'},
#         {'character_3': 'tiles/character_3.jpg'}
#     ]
# ]

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
    """
    Loads an image from the given path and resizes it to the specified size.

    Args:
        path (str): The file path to the image.
        size (tuple): The desired size of the image as (width, height).

    Returns:
        pg.Surface: The loaded and scaled image as a pygame Surface.
                    If the file is not found, returns a blank Surface with the specified size.

    Raises:
        FileNotFoundError: If the file at the given path cannot be located.
    """
    try:
        img = pg.image.load(path)
        return pg.transform.scale(img, size)
    except FileNotFoundError:
        print(f"Error: File not found {path}")
        return pg.Surface(size)


pieces = {
    "stick": {f"stick_{i}": f"tiles/stick_{i}.jpg" for i in range(1, 10)},
    "character": {f"character_{i}": f"tiles/character_{i}.jpg" for i in range(1, 10)},
    "dot": {f"dot_{i}": f"tiles/dot_{i}.jpg" for i in range(1, 10)},
    "wind": {f"wind_{i}": f"tiles/wind_{i}.jpg" for i in range(1, 5)},
    "dragon": {f"dragon_{i}": f"tiles/dragon_{i}.jpg" for i in range(1, 4)},
    "flower": {f"flower_{i}": f"tiles/flower_{i}.jpg" for i in range(1, 5)},
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
discarded = []


# Game state
clientsConnected = 0
game_started = False
lock = threading.Lock()
clients = []  # To store client connections
gameState = {
    "status": "ongoing",
    "turn": 0,
    "exposed": [[], [], [], []],
    "discarded": []
}


def broadcast_object(obj):
    """
    Send an object to all connected clients.

    This function serializes the given object using `pickle` and sends it to each client in the `clients` list.
    If sending the object fails for any client, the error is caught and printed.

    Args:
        obj: The object to be sent to all connected clients.
    """
    for client in clients:
        try:
            ob = pickle.dumps(obj)
            client.sendall(ob)
        except Exception as e:
            print(f"Failed to send object to client: {e}")


def broadcast(message):
    """
    Send a message(string) to all connected clients.

    This function serializes the given object using `pickle` and sends it to each client in the `clients` list.
    If sending the object fails for any client, the error is caught and printed.

    Args:
        message: The message to be sent to all connected clients.
    """

    for client in clients:
        try:
            client.sendall(message)
        except Exception as e:
            print(f"Failed to send message to client: {e}")


def broadcast_numbers():
    """
    Send the initial player numbers to all connected clients.

    This function serializes the given object using `pickle` and sends it to each client in the `clients` list.
    If sending the object fails for any client, the error is caught and printed.

    Args:
        None
    Returns:
        None
    """
    nums = [b"1", b"2", b"3", b"4"]
    for index, client in enumerate(clients):
        try:
            client.sendall(nums[index])
        except Exception as e:
            print(f"Failed to send player index to client: {e}")


def check_consecutive(arr):
    """
    Check if the elements in the list are consecutive integers.

    This function checks if each number in the list is one greater than the previous number and that no number exceeds 62.

    Args:
        arr (list): The list of integers to check.

    Returns:
        bool: True if the list contains consecutive integers and no number exceeds 62, otherwise False.
    """
    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] != 1 or arr[i] > 62:
            return False
    return True


def check_equal(arr):
    """
    Check if all elements in the list are equal and no number exceeds 83.

    This function checks if every element in the list is the same as the previous one and that no element exceeds 83.

    Args:
        arr (list): The list of integers to check.

    Returns:
        bool: True if all elements in the list are equal and no number exceeds 83, otherwise False.
    """
    for i in range(1, len(arr)):
        if arr[i] - arr[i - 1] != 0 or arr[i] > 83:
            return False
    return True


def check_gong(cards, target):
    """
    Check if a 'gong' can be formed by adding a target card to any four equal cards in the list.

    This function checks if adding a given target card to any sequence of four consecutive identical cards
    in the list results in a valid 'gong', which is a sequence of equal values (after converting
    the cards to their corresponding values).

    Args:
        cards (list): A list of card identifiers.
        target (int): The card to be added to the sequence of three cards.

    Returns:
        int: The index where the 'gong' can be formed (if found), otherwise -1.
    """
    for i in range(len(cards) - 2):
        partition = cards[i:i + 3]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        gong = check_equal(newPartition)
        if gong:
            return i
    return -1


def check_pong(cards, target):
    """
    Check if a 'pong' can be formed by adding a target card to any three identical cards in the list.

    This function checks if adding a given target card to any sequence of three consecutive identical cards
    in the list results in a valid 'pong', which is a sequence of equal values (after converting
    the cards to their corresponding values).

    Args:
        cards (list): A list of card identifiers.
        target (int): The card to be added to the sequence of three cards.

    Returns:
        int: The index where the 'pong' can be formed (if found), otherwise -1.
    """
    for i in range(len(cards) - 1):
        partition = cards[i:i + 2]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        pong = check_equal(newPartition)
        if pong:
            return i
    return -1


def check_seung(cards, target):
    """
    Check if a 'seung' can be formed by adding a target card to any three consecutive cards in the list.

    This function checks if adding a given target card to any sequence of three consecutive by value cards
    in the list results in a valid 'seung', which is a sequence of equal values (after converting
    the cards to their corresponding values).

    Args:
        cards (list): A list of card identifiers.
        target (int): The card to be added to the sequence of three cards.

    Returns:
        int: The index where the 'seung' can be formed (if found), otherwise -1.
    """
    for i in range(len(cards) - 1):
        partition = cards[i:i + 2]
        partition.append(target)
        newPartition = []
        for card in partition:
            newPartition.append(values[card])
        newPartition.sort()
        seung = check_consecutive(newPartition)
        if seung:
            return i
    return -1


def check_pair(card_1, card_2):
    """
    Check if two cards form a pair, i.e., they have equal values.

    This function checks if the values of two cards are equal, indicating that they form a valid pair.

    Args:
        card_1 (int): The first card identifier.
        card_2 (int): The second card identifier.

    Returns:
        bool: True if the cards form a pair (have equal values), otherwise False.
    """
    return values[card_1] - values[card_2] == 0


def check_winning(cards):
    """
    Check if the given set of cards forms a valid winning hand.

    This function checks whether the given list of cards forms a valid combination
    according to the game's rules. A winning hand consists of groups of 3 consecutive cards
    or 3 identical cards, as well as one pair of identical cards.

    Args:
        cards (list): A list of card identifiers representing the player's cards.

    Returns:
        bool: True if the cards form a valid winning hand, otherwise False.
    """
    for i in range(0, len(cards), 3):
        part = cards[i:i + 3]

        if len(part) == 3:
            newPartition = []
            for card in part:
                newPartition.append(values[card])
            newPartition.sort()
            if not (check_consecutive(newPartition)
                    or check_equal(newPartition)):
                return False
        elif len(part) == 2:
            if not check_pair(part[0], part[1]):
                return False
    return True


def expose_cards(index, player, nr_cards, target):
    """
    Expose a subset of cards from a player's hand and update the game state.

    This function exposes a selected number of cards from the given player's hand,
    appends a target card, and updates the game state. The exposed cards are then
    removed from the player's hand.

    Args:
        index (int): The starting index in the player's hand to expose cards from.
        player (int): The index of the player (1-based index).
        nr_cards (int): The number of cards to expose (after excluding the target card).
        target (str): The card to append to the exposed set.

    Updates:
        gameState["exposed"]: Adds the exposed cards for the specified player.
        players: Removes the exposed cards from the player's hand.
    """
    global gameState, players
    nr_cards -= 1

    to_append = players[player - 1][index:index + nr_cards]

    to_append.append(target)
    to_append = sorted(to_append, key=lambda x: next(iter(x)))

    gameState["exposed"][player - 1].extend(to_append)

    new_player_cards = players[player - 1][:index] + \
        players[player - 1][index + nr_cards:]
    players[player - 1] = new_player_cards


def send_cards_to_players():
    """
    Send the cards of all players to their respective clients.

    This function serializes the list of cards for each player and sends the data
    to the corresponding client over the network.

    Updates:
        - Each player's cards are sent to their associated client.

    Exception Handling:
        - If sending cards fails, an error message is printed for the respective player.
    """
    for index, client in enumerate(clients):
        try:
            cards = pickle.dumps(players[index])
            client.sendall(cards)
        except Exception as e:
            print(f"Failed to send cards to player: {e}")


def send(conn, message):
    """
    Send a serialized message to a client over the provided connection.

    Args:
        conn (socket): The connection object representing the client.
        message (object): The message to be sent, which will be serialized using pickle.

    This function serializes the provided message using pickle and sends it
    over the provided connection using the `sendall` method.
    """
    toSend = pickle.dumps(message)
    conn.sendall(toSend)


def handle_player(player, conn):
    """
    This function handles different actions from a player during the game.
    It processes actions such as drawing, picking, discarding, and checking for a winning hand.

    Args:
        player (int): The ID of the player sending the request.
        conn (socket): The socket connection through which the player sends requests and receives messages.

    Returns:
        None: This function doesn't return any value. It sends messages to the client and updates the game state.

    Raises:
        Exception: If any unexpected exception occurs during the communication or processing of the request.
    """
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
        if gameState["turn"] < 4:
            found = False
            how_many = 0
            index = gameState["turn"]
            for i, card in enumerate(players[index]):
                name = list(card.keys())[0]
                if values[name] >= 100:
                    gameState["exposed"][index].append(players[index][i])
                    players[index].pop(i)
                    found = True
                    how_many += 1
            if found:
                message = {
                    "type": "flower",
                    "content": [how_many, players[index]]
                }
                send(clients[index], message)
                message = {
                    "type": "state",
                    "content": gameState
                }
                broadcast_object(message)

        try:
            data = conn.recv(1024)
            if data:
                request = pickle.loads(data)
                if request["action"] == "draw":
                    if request["player"] != gameState["turn"] % 4 + 1:
                        message = {
                            "type": "warning",
                            "content": "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn, message)
                    else:
                        newCard = all_cards.pop()
                        ind = request["player"] - 1
                        playerCards = request["args"][0]
                        value = values[list(newCard.keys())[0]]
                        players[ind] = playerCards
                        if value < 100:
                            playerCards.append(newCard)
                            players[ind] = playerCards
                            message = {
                                "type": "drawn",
                                "content": players[ind]
                            }
                            send(conn, message)
                        else:
                            gameState["exposed"][ind].append(newCard)
                            message = {
                                "type": "flower-draw",
                                "content": [0, players[ind]]
                            }
                            send(conn, message)
                            message = {
                                "type": "state",
                                "content": gameState
                            }
                            broadcast_object(message)

                if request["action"] == "pick":

                    if len(discarded) == 0:
                        message = {
                            "type": "warning",
                            "content": "There are no discards"
                        }
                        send(conn, message)
                    else:
                        playerCards = request["args"][0]
                        rawTarget = discarded[-1]
                        target = list(discarded[-1].keys())[0]
                        cards = [list(card.keys())[0] for card in playerCards]
                        players[player - 1] = playerCards
                        cards_to_expose = 0
                        index = -1
                        # check if a gong can happen
                        gong = check_gong(cards, target)

                        if gong >= 0:
                            message = {
                                "type": "warning",
                                "content": "GONG"
                            }
                            send(conn, message)
                            message = {
                                "type": "flower",
                                "content": [0, players[index]]
                            }
                            send(clients[index], message)
                            cards_to_expose = 4
                            index = gong
                        else:
                            pong = check_pong(cards, target)
                            if pong >= 0:
                                message = {
                                    "type": "warning",
                                    "content": "PONG"
                                }
                                send(conn, message)
                                cards_to_expose = 3
                                index = pong
                            else:
                                seung = check_seung(
                                    cards,
                                    target) if request["player"] == gameState["turn"] % 4 + 1 else -1
                                if seung >= 0:
                                    message = {
                                        "type": "warning",
                                        "content": "SEUNG"
                                    }
                                    send(conn, message)
                                    cards_to_expose = 3
                                    index = seung
                                else:
                                    message = {
                                        "type": "warning",
                                        "content": "No pong/gong/seung"
                                    }
                                    send(conn, message)
                        if index >= 0:
                            expose_cards(
                                index, request["player"], cards_to_expose, rawTarget)
                            # discarded.pop()
                            gameState["discarded"].pop()
                            message = {
                                "type": "state",
                                "content": gameState
                            }
                            broadcast_object(message)
                            message = {
                                "type": "drawn",
                                "content": players[request["player"] - 1]
                            }
                            send(conn, message)

                if request["action"] == "discard":
                    if request["player"] != gameState["turn"] % 4 + 1:
                        message = {
                            "type": "warning",
                            "content": "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn, message)
                    else:
                        cardIndex = request["args"][1]
                        playerCards = request["args"][0]

                        player = request["player"]
                        print(playerCards[cardIndex])
                        discarded.append(playerCards[cardIndex])
                        playerCards.pop(cardIndex)
                        players[player - 1] = playerCards
                        message = {
                            "type": "discarded",
                            "content": players[player - 1]
                        }
                        send(conn, message)
                        gameState["turn"] = gameState["turn"] + 1
                        gameState["discarded"] = discarded

                        message = {
                            "type": "state",
                            "content": gameState
                        }

                        broadcast_object(message)
                if request["action"] == "check":
                    if request["player"] != gameState["turn"] % 4 + 1:
                        message = {
                            "type": "warning",
                            "content": "It's not your turn!"
                        }
                        print(f"Sent warning to player {request["player"]}")
                        send(conn, message)
                    else:
                        playerCards = request["args"][0]
                        modified = []
                        for card in playerCards:
                            modified.append(list(card.keys())[0])
                        check = check_winning(modified)
                        if check:
                            message = {
                                "type": "win",
                                "content": request["player"]
                            }
                            broadcast_object(message)
                        else:
                            message = {
                                "type": "warning",
                                "content": "Not a winning hand!"
                            }
                            send(conn, message)

        except Exception as e:
            print(f"Some exception occured: {e}")


def handle_game():
    """
    Main game loop to handle player actions.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If an error occurs in handling player connections or game state.
    """
    global gameState, clients
    for index, conn in enumerate(clients):
        threading.Thread(
            target=handle_player,
            args=(
                index + 1,
                conn),
            daemon=True).start()


def wait_for_client_responses(expected_clients):
    """
    Wait for all clients to send their 'ready' response.

    Args:
        expected_clients (int): The number of clients expected to respond with 'ready'.

    Returns:
        None

    Raises:
        Exception: If there is an error receiving data from a client.
    """
    responses = 0
    while responses < expected_clients:
        for conn in clients:
            try:
                data = conn.recv(1024)
                if data == b"ready":
                    responses += 1
                    print(
                        f"Client {conn} is ready. Total ready: {responses}/{expected_clients}")
            except Exception as e:
                print(f"Error receiving client response: {e}")
    print("All clients are ready.")


def main():
    """
    Main server loop to handle client connections and start the game when 4 clients are connected.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If there is an error during client connection or handling.
    """
    global clientsConnected
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        # Start the client handler thread which will start processing clients
        # once 4 clients are connected

        while True:
            conn, addr = s.accept()
            with lock:
                clientsConnected += 1
                clients.append(conn)
                print(f"Connected by {addr}")

                if clientsConnected == 4:
                    print("4 clients connected. The game is starting.")
                    broadcast_numbers()  # announces players what is their turn
                    wait_for_client_responses(4)
                    send_cards_to_players()
                    threading.Thread(target=handle_game, daemon=True).start()
                elif clientsConnected > 4:
                    print("Game is full. No more connections are allowed.")
                    conn.sendall(
                        b"Game is full. No more connections are allowed.")
                    conn.close()


if __name__ == "__main__":
    main()
