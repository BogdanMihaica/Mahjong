import pygame as pg
import random
import socket
import threading
import pickle
import queue

# Socket configuration
HOST = "127.0.0.1"
PORT = 65432

# Game start
player_won = 0
message_queue = queue.Queue()
gameStarted = False
player = 0
playerCards = []
lock = 0
draws = 1
tile_size = (36, 50)
shouldDiscard = False
gameState = {
    "status": "ongoing",
    "turn": 0,
    "exposed": [[], [], [], []],
    "discarded": []
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


def transform_cards(cards):
    """
    Transforms a list of card dictionaries by loading and scaling their associated images.

    Args:
        cards (list): A list of dictionaries, where each dictionary has a single key-value pair.
                      The key represents the card identifier, and the value is the file path to the card's image.

    Returns:
        list: A list of dictionaries with the same keys, but the values are pygame Surfaces
              representing the loaded and scaled images.

    Raises:
        FileNotFoundError: If any image file cannot be located during loading.
    """
    crs = []
    for card in cards:
        key = list(card.keys())[0]
        val = card[key]
        crs.append({key: load_image(val, tile_size)})
    return crs


def handle_wait(conn):
    """
    Handles the waiting state of the game until it starts, receiving and processing data from the connection.

    Args:
        conn (socket.socket): The socket connection to communicate with the server or other player.

    Returns:
        None

    Raises:
        Exception: Catches and logs any exceptions that occur during data handling or communication.
    """
    global gameStarted, playerCards, player
    while not gameStarted:
        try:
            data = conn.recv(1024)
            if int(data):
                player = int(data)
                print(player)
                toSend = b"ready"
                conn.sendall(toSend)
                gameStarted = True
                # sending cards to players
                card_data = conn.recv(4096)
                cards = pickle.loads(card_data)
                playerCards = transform_cards(cards)
                print(playerCards)
        except Exception as e:
            print(f"Some exception occurred: {e}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    pg.init()
    pg.display.set_caption(f"Mahjong")
    # Board Configuration
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700

    GREEN = (44, 87, 36)
    WHITE = (227, 227, 227)
    GRAY = (50, 50, 50)
    BLUE = (81, 94, 158)

    window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    try:
        bg_image = pg.image.load("bg.png")
        bg_image = pg.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        print("Error: bg.png not found!")
        pg.quit()
        exit()

    tile_size = (36, 50)
    pieces = {
        "stick": {
            f"stick_{i}": load_image(
                f"tiles/stick_{i}.jpg",
                tile_size) for i in range(
                1,
                10)},
        "character": {
            f"character_{i}": load_image(
                f"tiles/character_{i}.jpg",
                tile_size) for i in range(
                1,
                10)},
        "dot": {
            f"dot_{i}": load_image(
                f"tiles/dot_{i}.jpg",
                tile_size) for i in range(
                1,
                10)},
        "wind": {
            f"wind_{i}": load_image(
                f"tiles/wind_{i}.jpg",
                tile_size) for i in range(
                1,
                5)},
        "dragon": {
            f"dragon_{i}": load_image(
                f"tiles/dragon_{i}.jpg",
                tile_size) for i in range(
                1,
                4)},
        "flower": {
            f"flower_{i}": load_image(
                f"tiles/flower_{i}.jpg",
                tile_size) for i in range(
                1,
                5)},
        "season": {
            f"season_{i}": load_image(
                f"tiles/season_{i}.jpg",
                tile_size) for i in range(
                1,
                5)},
    }
    hidden = load_image("tiles/blank.jpg", tile_size),

    def paint_piece(x_offset, y_offset, img, rotation=0):
        """
        Draws a game piece on the window with optional rotation and returns its rectangular area.

        Args:
            x_offset (int): The x-coordinate offset for positioning the image.
            y_offset (int): The y-coordinate offset for positioning the image.
            img (pg.Surface): The pygame Surface representing the piece to be drawn.
            rotation (int, optional): The angle in degrees to rotate the image. Defaults to 0.

        Returns:
            pg.Rect: A pygame Rect object representing the rectangular area of the piece.

        Raises:
            None
        """
        if rotation:
            img = pg.transform.rotate(img, rotation)
        window.blit(img, (x_offset, y_offset))
        return pg.Rect(x_offset, y_offset, tile_size[0], tile_size[1])

    def display_pieces(
            all_cards,
            x_offset,
            y_offset,
            orientation="horizontal",
            player=1,
            rotation=0):
        """
        Displays a set of game pieces on the screen with specified alignment and returns their rectangular areas.

        Args:
            all_cards (list): A list of card dictionaries, where each dictionary contains
                            the card name as the key and its image as the value.
            x_offset (int): The initial x-coordinate offset for positioning the pieces.
            y_offset (int): The initial y-coordinate offset for positioning the pieces.
            orientation (str, optional): The layout direction for the pieces. Can be "horizontal" or "vertical".
                                        Defaults to "horizontal".
            player (int, optional): The player ID. If not 1, a hidden card image is displayed instead. Defaults to 1.
            rotation (int, optional): The angle in degrees to rotate the pieces. Defaults to 0.

        Returns:
            list: A list of tuples, where each tuple contains a pygame Rect representing the piece's rectangular area
                and the corresponding card dictionary.

        Raises:
            None
        """
        spacing = 10
        card_rects = []
        for card in all_cards:
            for name, img in card.items():
                rect = paint_piece(
                    x_offset,
                    y_offset,
                    img if player == 1 else hidden[0],
                    rotation)
                card_rects.append((rect, card))
                if orientation == "horizontal":
                    x_offset += tile_size[0] + spacing
                else:
                    y_offset += tile_size[0] + spacing
        return card_rects

    def display_exposed_cards():
        """
        Displays the exposed cards of all players on the screen based on their relative positions.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        global gameState, player

        position_mapping = {
            1: {"left": 4, "top": 3, "right": 2, "bottom": 1},
            2: {"left": 1, "top": 4, "right": 3, "bottom": 2},
            3: {"left": 2, "top": 1, "right": 4, "bottom": 3},
            4: {"left": 3, "top": 2, "right": 1, "bottom": 4},
        }

        exposed = gameState["exposed"]
        tile_width = tile_size[1]
        padX = 20
        s2w = SCREEN_HEIGHT - 40

        rotations = {
            "left": 90,
            "top": 180,
            "right": 270,
            "bottom": 0,
        }
        areas = {
            "left": (
                padX,
                20,
                "vertical"),
            "top": (
                (SCREEN_WIDTH - s2w) // 2,
                padX,
                "horizontal"),
            "right": (
                SCREEN_WIDTH - padX - tile_width,
                20,
                "vertical"),
            "bottom": (
                (SCREEN_WIDTH - s2w) // 2,
                SCREEN_HEIGHT - padX - tile_width,
                "horizontal"),
        }

        relative_positions = position_mapping[player]

        for position, player_idx in relative_positions.items():
            x, y, orientation = areas[position]
            cards = exposed[player_idx - 1]

            if orientation == "horizontal":
                x_offset, y_offset = center_pieces(
                    cards, SCREEN_WIDTH, orientation)
                x_offset += 0
                y_offset = y
            else:
                x_offset, y_offset = center_pieces(
                    cards, SCREEN_HEIGHT, orientation)
                x_offset = x
                y_offset += 0

            rotation = rotations[position]
            display_pieces(
                transform_cards(cards),
                x_offset,
                y_offset,
                orientation,
                rotation=rotation
            )

    def card_action(x, y, color1):
        """
        Highlights a card on the screen by overlaying a semi-transparent rectangle.

        Args:
            x (int): The x-coordinate of the top-left corner of the rectangle.
            y (int): The y-coordinate of the top-left corner of the rectangle.
            color1 (tuple): A tuple representing the RGB color of the rectangle. The alpha channel is added automatically.

        Returns:
            None

        Raises:
            None
        """
        rect_surface = pg.Surface((tile_size[0], tile_size[1]), pg.SRCALPHA)
        color = (color1[0], color1[1], color1[2], 128)
        rect_surface.fill(color)
        window.blit(rect_surface, (x, y))

    def center_pieces(player_cards, screen_dim, orientation):
        """
        Calculates the offsets required to center a set of cards on the screen based on the specified orientation.

        Args:
            player_cards (list): A list of cards to be displayed.
            screen_dim (int): The dimension of the screen (width or height) depending on the orientation.
            orientation (str): The orientation of the cards, either "horizontal" or "vertical".

        Returns:
            tuple: A tuple containing the x-offset and y-offset. One of the values will be `None` based on the orientation.

        Raises:
            None
        """
        total_width = len(player_cards) * (tile_size[0] + 10) - 10
        if orientation == "horizontal":
            return (screen_dim - total_width) // 2, None
        else:
            return None, (screen_dim - total_width) // 2

    def text(x, y, fontsize, message, color=(255, 255, 255)):
        """
        Renders and displays a text message on the screen at a specified position with a specified font size and color.

        Args:
            x (int): The x-coordinate of the center of the text.
            y (int): The y-coordinate of the center of the text.
            fontsize (int): The font size of the text.
            message (str): The message to be displayed.
            color (tuple, optional): A tuple representing the RGB color of the text. Defaults to white (255, 255, 255).

        Returns:
            None

        Raises:
            None
        """
        font = pg.font.SysFont("timesnewroman", fontsize)
        rendered_text = font.render(message, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        window.blit(rendered_text, text_rect)

    def display_draw_area():
        """
        Renders a semi-transparent rectangle representing the draw area on the screen,
        including a border and a centered "Draw card" text.

        Args:
            None

        Returns:
            pg.Rect: A pygame Rect representing the area where the draw card button is located.

        Raises:
            None
        """
        surfaceW, surfaceH = 200, 200
        x, y = 150, SCREEN_HEIGHT // 2 - surfaceH // 2 - 100
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (0, 255, 0, 70)
        surface.fill(color)
        border_color = (0, 255, 0)
        border_thickness = 5
        pg.draw.rect(
            surface,
            border_color,
            surface.get_rect(),
            border_thickness)
        window.blit(surface, (x, y))
        text_x = x + surfaceW // 2
        text_y = y + surfaceH // 2
        text(text_x, text_y, 30, "Draw card", color=(0, 255, 0))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def display_discard_button():
        """
        Renders a semi-transparent rectangle representing the discard button on the screen,
        including a border and a centered "Discard" text.

        Args:
            None

        Returns:
            pg.Rect: A pygame Rect representing the area where the discard button is located.

        Raises:
            None
        """
        surfaceW, surfaceH = 200, 80
        x, y = 150, SCREEN_HEIGHT // 2 - surfaceH // 2 + 150 + 10 - 100
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (255, 0, 0, 70)
        surface.fill(color)
        border_color = (255, 0, 0)
        border_thickness = 5
        pg.draw.rect(
            surface,
            border_color,
            surface.get_rect(),
            border_thickness)
        window.blit(surface, (x, y))
        text_x = x + surfaceW // 2
        text_y = y + surfaceH // 2
        text(text_x, text_y, 30, "Discard", color=(255, 0, 0))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def display_pick_last_button():
        """
        Renders a semi-transparent rectangle representing the "Pick last card" button on the screen,
        including a border and a centered "Pick last card" text.

        Args:
            None

        Returns:
            pg.Rect: A pygame Rect representing the area where the "Pick last card" button is located.

        Raises:
            None
        """
        surfaceW, surfaceH = 200, 80
        x, y = 150, SCREEN_HEIGHT // 2 - surfaceH // 2 + 150 + 10
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (0, 0, 255, 70)
        surface.fill(color)
        border_color = (0, 0, 255)
        border_thickness = 5
        pg.draw.rect(
            surface,
            border_color,
            surface.get_rect(),
            border_thickness)
        window.blit(surface, (x, y))
        text_x = x + surfaceW // 2
        text_y = y + surfaceH // 2
        text(text_x, text_y, 20, "Pick last card", color=(255, 255, 255))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def request(message):
        """
        Sends a serialized message to the server via a socket connection.

        Args:
            message (any): The message to be sent to the server. It will be serialized using pickle.

        Returns:
            None

        Raises:
            None
        """
        toSend = pickle.dumps(message)
        s.sendall(toSend)

    def display_warning(message):
        """
        Renders a semi-transparent rectangle representing a warning message on the screen,
        including a red background and the given message in white text.

        Args:
            message (str): The warning message to display on the screen.

        Returns:
            pg.Rect: A pygame Rect representing the area where the warning message is located.

        Raises:
            None
        """
        surfaceW, surfaceH = 400, 40
        x, y = 380, SCREEN_HEIGHT // 2 - surfaceH // 2 + 150 + 30
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (255, 0, 0, 255)
        surface.fill(color)
        window.blit(surface, (x, y))
        text_x = x + surfaceW // 2
        text_y = y + surfaceH // 2
        text(text_x, text_y, 30, message, color=(255, 255, 255))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def display_exposed_areas():
        """
        Renders four semi-transparent areas around the screen's edges to visually represent
        exposed areas in the game. These areas are drawn as rectangles with a white background.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        padX = 20
        s1h = SCREEN_HEIGHT - 40
        s1w = tile_size[1]
        surface = pg.Surface((s1w, s1h), pg.SRCALPHA)
        color = (255, 255, 255, 70)
        surface.fill(color)
        x, y = padX, 20
        window.blit(surface, (x, y))
        x, y = SCREEN_WIDTH - padX - tile_size[1], 20
        window.blit(surface, (x, y))

        s2h = tile_size[1]
        s2w = SCREEN_HEIGHT - 40
        surface = pg.Surface((s2w, s2h), pg.SRCALPHA)
        color = (255, 255, 255, 70)
        surface.fill(color)
        x, y = (SCREEN_WIDTH - s2w) // 2, padX
        window.blit(surface, (x, y))
        x, y = (SCREEN_WIDTH - s2w) // 2, SCREEN_HEIGHT - padX - tile_size[1]
        window.blit(surface, (x, y))
        return

    def display_discarded_cards_area():
        """
        Renders a semi-transparent area on the screen to represent the discarded cards region.
        This area is drawn as a rectangle with a black background and some transparency.

        Args:
            None

        Returns:
            pg.Rect: The rectangle representing the discarded cards area.

        Raises:
            None
        """
        surfaceW, surfaceH = 500, 400
        x, y = 380, SCREEN_HEIGHT // 2 - surfaceH // 2 - 50
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (0, 0, 0, 30)
        surface.fill(color)
        window.blit(surface, (x, y))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def display_discarded_cards():
        """
        Renders the discarded cards area on the screen, displaying all the discarded cards.
        The cards are arranged in rows and columns with a defined padding between them.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        global gameState
        cards = transform_cards(gameState["discarded"])
        offsetX, offsetY = 380, SCREEN_HEIGHT // 2 - 400 // 2 - 50
        padding = 10
        cards_per_row = 11
        for i, card in enumerate(cards):
            card_name = list(card.keys())[0]
            surface = card[card_name]
            x = offsetX + (i %
                           cards_per_row) * tile_size[0] + padding * (i %
                                                                      cards_per_row)
            y = offsetY + (i // cards_per_row) * \
                tile_size[1] + padding * (i // cards_per_row)
            paint_piece(x, y, surface, 0)

    def deserialize_cards(cards):
        """
        Converts a list of card dictionaries to a list of dictionaries with image file paths.
        Each card's key is used to form the corresponding image file path in the format `tiles/{card_name}.jpg`.

        Args:
            cards (list): A list of card dictionaries, each with a single key representing the card's name.

        Returns:
            list: A list of dictionaries, each with a key representing the card's name and a value
                representing the corresponding image file path.

        Raises:
            None
        """
        d_cards = []
        for card in cards:
            d_cards.append(
                {list(card.keys())[0]: f"tiles/{list(card.keys())[0]}.jpg"})
        return d_cards

    def display_check_win():
        """
        Displays a button-like area on the screen labeled "Check win".
        This area is used for checking the current win status in the game.

        The button has a yellow semi-transparent background with a border and the label in white text.

        Returns:
            pg.Rect: The rectangle representing the area of the "Check win" button.
        """
        surfaceW, surfaceH = 200, 50
        x, y = 150, SCREEN_HEIGHT // 2 - surfaceH // 2 - 230
        surface = pg.Surface((surfaceW, surfaceH), pg.SRCALPHA)
        color = (255, 255, 0, 70)
        surface.fill(color)
        border_color = (255, 255, 0)
        border_thickness = 5
        pg.draw.rect(
            surface,
            border_color,
            surface.get_rect(),
            border_thickness)
        window.blit(surface, (x, y))
        text_x = x + surfaceW // 2
        text_y = y + surfaceH // 2
        text(text_x, text_y, 20, "Check win", color=(255, 255, 255))
        return pg.Rect(x, y, surfaceW, surfaceH)

    def handle_messages():
        """
        Continuously listens for incoming messages from the server and processes them based on their type.

        The function reads data from the socket, deserializes it using `pickle`, and processes the message depending on the
        message type. It updates the game state, player cards, and other game variables accordingly.

        It handles the following message types:
            - "drawn": Updates player cards and manages the draw count.
            - "warning": Displays a warning message.
            - "discarded": Updates player cards after a discard action.
            - "flower": Updates player cards and manages the draw count with a flower card.
            - "state": Updates the global game state.
            - "win": Marks the player as the winner.

        Any errors during message reception are caught and printed.
        """
        global gameState, message_queue, playerCards, active_warning, shouldDiscard, draws, player_won
        while True:
            try:
                data = s.recv(4096)
                message = pickle.loads(data)
                message_queue.put(message)

                if message["type"] == "drawn":
                    playerCards = transform_cards(message["content"])
                    draws -= 1
                    if draws == 0:
                        shouldDiscard = True
                elif message["type"] == "warning":
                    print("i got warned")
                    active_warning = message["content"]
                elif message["type"] == "discarded":
                    playerCards = transform_cards(message["content"])
                    shouldDiscard = False
                elif message["type"] == "flower":
                    playerCards = transform_cards(message["content"][1])
                    draws += message["content"][0]
                elif message["type"] == "state":
                    gameState = message["content"]
                elif message["type"] == "win":
                    player_won = message["content"]

            except Exception as e:
                print(f"Exeption while receiving broadcast: {e}")

    threading.Thread(target=handle_wait, args=(s,), daemon=True).start()
    run = True
    holdingCard = False
    heldCard = 0
    heldCardIndex = 0
    heldCardX = 0
    heldCardY = 0
    captionSet = False
    active_warning = "none"
    pickSound = pg.mixer.Sound("sounds/pick.wav")
    threading.Thread(target=handle_messages, daemon=True).start()
    if gameState["turn"] == 0 and player == 1:
        draws = 0
    while run:

        draw = None
        discard = None
        pick = None
        window.blit(bg_image, (0, 0))

        if not gameStarted:
            text(500, 350, 50, "Waiting for players")
        elif player_won > 0:
            window.blit(bg_image, (0, 0))
            text(500, 350, 50, f"Player {player_won} won the game!")
        else:
            if not captionSet:
                pg.display.set_caption(f"Mahjong - Player {player}")
                captionSet = True
            if draws > 0:
                shouldDiscard = False
            else:
                shouldDiscard = True
            # if gameState["turn"]==0 and player==1:
            #     shouldDiscard=True
            if active_warning != "none":
                display_warning(active_warning)
            display_discarded_cards_area()
            display_discarded_cards()
            check = display_check_win()
            draw = display_draw_area()
            discard = display_discard_button()
            pick = display_pick_last_button()
            display_exposed_areas()
            display_exposed_cards()
            x_offset, _ = center_pieces(
                playerCards, SCREEN_WIDTH, "horizontal")
            player1_rects = display_pieces(
                playerCards,
                x_offset,
                SCREEN_HEIGHT -
                tile_size[1] -
                80,
                "horizontal",
                rotation=0)

            # Draw the highlight rectangle if holding a card
            if holdingCard:
                select_color = (255, 253, 117)
                card_action(heldCardX, heldCardY, select_color)

            # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and gameStarted:
                mouse_pos = pg.mouse.get_pos()

                # Check card pick
                for index, player_rect in enumerate(player1_rects):
                    rect = player_rect[0]
                    card = player_rect[1]
                    if rect.collidepoint(mouse_pos):
                        if not holdingCard:
                            pickSound.play()
                            holdingCard = True
                            card_name = list(card.keys())[0]
                            heldCard = card_name
                            heldCardIndex = index
                            heldCardX, heldCardY = rect.topleft[0], rect.topleft[1]
                        else:
                            holdingCard = False
                            playerCards[heldCardIndex], playerCards[index] = playerCards[index], playerCards[heldCardIndex]
                        break

                # Check Draw Card click
                if draw.collidepoint(mouse_pos):
                    if (shouldDiscard == False and draws >= 1) or (
                            gameState["turn"] == 0 and player == 1 and draws > 0):
                        message = {
                            "player": player,
                            "action": "draw",
                            "args": [deserialize_cards(playerCards)]
                        }
                        request(message)
                    else:
                        active_warning = "You can't do this now."

                # Check Pick Last Card click
                if pick.collidepoint(mouse_pos):
                    message = {
                        "player": player,
                        "action": "pick",
                        "args": [deserialize_cards(playerCards)]
                    }
                    request(message)

                # Check Discard click
                if discard.collidepoint(mouse_pos):
                    if not holdingCard:
                        active_warning = "You should select a card first!"
                    elif shouldDiscard == False:
                        active_warning = "You can't discard now"
                    elif draws >= 1:
                        active_warning = "You still need to draw"
                    else:
                        print(shouldDiscard)
                        message = {
                            "player": player, "action": "discard", "args": [
                                deserialize_cards(playerCards), heldCardIndex]}
                        request(message)
                        holdingCard = False
                if check.collidepoint(mouse_pos):
                    message = {
                        "player": player,
                        "action": "check",
                        "args": [deserialize_cards(playerCards)]
                    }
                    request(message)
        pg.display.update()

    pg.quit()
