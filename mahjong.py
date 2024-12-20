import pygame as pg
import random

pg.init()

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

def load_image(path, size):
    try:
        img = pg.image.load(path)
        return pg.transform.scale(img, size)
    except FileNotFoundError:
        print(f"Error: File not found {path}")
        return pg.Surface(size)

tile_size = (36, 50)
pieces = {
    "stick": {f"stick_{i}": load_image(f"tiles/stick_{i}.jpg", tile_size) for i in range(1, 10)},
    "character": {f"character_{i}": load_image(f"tiles/character_{i}.jpg", tile_size) for i in range(1, 10)},
    "dot": {f"dot_{i}": load_image(f"tiles/dot_{i}.jpg", tile_size) for i in range(1, 10)},
    "wind": {f"wind_{i}": load_image(f"tiles/wind_{i}.jpg", tile_size) for i in range(1, 5)},
    "dragon": {f"dragon_{i}": load_image(f"tiles/dragon_{i}.jpg", tile_size) for i in range(1, 4)},
    "flower": {f"flower_{i}": load_image(f"tiles/flower_{i}.jpg", tile_size) for i in range(1, 5)},
    "season": {f"season_{i}": load_image(f"tiles/season_{i}.jpg", tile_size) for i in range(1, 5)},
}
hidden=load_image("tiles/blank.jpg",tile_size),
def paint_piece(x_offset, y_offset, img, rotation=0):
    if rotation:
        img = pg.transform.rotate(img, rotation)
    window.blit(img, (x_offset, y_offset))
    return pg.Rect(x_offset, y_offset, tile_size[0], tile_size[1])

# Shuffling cards
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

for key in pieces:
    iterations = 4
    if key in ["flower", "season"]:
        iterations = 2
    for _ in range(iterations):
        for key1 in pieces[key]:
            all_cards.append({key1: pieces[key][key1]})

def display_pieces(all_cards, x_offset, y_offset, orientation="horizontal",player=1, rotation=0):
    spacing = 10
    card_rects = []
    for card in all_cards:
        for name, img in card.items():
            rect = paint_piece(x_offset, y_offset, img if player == 1 else hidden[0], rotation)
            card_rects.append((rect, card))
            if orientation == "horizontal":
                x_offset += tile_size[0] + spacing
            else:
                y_offset += tile_size[0] + spacing
    return card_rects

random.shuffle(all_cards)
player1 = all_cards[0:14]
player2 = all_cards[14:27]
player3 = all_cards[27:40]
player4 = all_cards[40:53]
drawable = all_cards[52:]

def card_action(x,y, color1):
    rect_surface = pg.Surface((tile_size[0], tile_size[1]), pg.SRCALPHA)
    color = (color1[0], color1[1], color1[2], 128)
    rect_surface.fill(color)
    window.blit(rect_surface, (x, y))

def center_pieces(player_cards, screen_dim, orientation):
    total_width = len(player_cards) * (tile_size[0] + 10) - 10
    if orientation == "horizontal":
        return (screen_dim - total_width) // 2, None
    else:
        return None, (screen_dim - total_width) // 2

run = True
holdingCard=False
heldCard=0
heldCardIndex=0
heldCardX=0
heldCardY=0
pickSound = pg.mixer.Sound("sounds/pick.wav")
while run:
    # Clear and redraw the background
    window.blit(bg_image, (0, 0))

    # Draw all players' pieces
    x_offset, _ = center_pieces(player1, SCREEN_WIDTH, "horizontal")
    player1_rects = display_pieces(player1, x_offset, SCREEN_HEIGHT - tile_size[1] - 20, "horizontal", rotation=0)

    _, y_offset = center_pieces(player2, SCREEN_HEIGHT, "vertical")
    player2_rects = display_pieces(player2, SCREEN_WIDTH - tile_size[1] - 20, y_offset, "vertical", player=2, rotation=90)

    x_offset, _ = center_pieces(player3, SCREEN_WIDTH, "horizontal")
    player3_rects = display_pieces(player3, x_offset, 20, "horizontal", player=3, rotation=180)

    _, y_offset = center_pieces(player4, SCREEN_HEIGHT, "vertical")
    player4_rects = display_pieces(player4, 20, y_offset, "vertical", player=4, rotation=270)

    # Draw the highlight rectangle if holding a card
    if holdingCard:
        select_color = (255, 253, 117)
        card_action(heldCardX, heldCardY, select_color)

    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            for index, player_rect in enumerate(player1_rects):
                rect = player_rect[0]
                card = player_rect[1]
                if rect.collidepoint(mouse_pos):
                    if not holdingCard:
                        
                        pickSound.play()
                        holdingCard = True
                        card_name = list(card.keys())[0]
                        print(f"Grabbed card: {card_name}. Card value: {values[card_name]}. Card Index: {index}")
                        heldCard = card_name
                        heldCardIndex = index
                        heldCardX, heldCardY = rect.topleft[0], rect.topleft[1]
                    else:
                        holdingCard = False
                        player1[heldCardIndex], player1[index] = player1[index], player1[heldCardIndex]
                        print(f"Dropped card: {heldCard}, card index: {heldCardIndex} on card: {card_name}, card Index: {index}")
                    break
    pg.display.update()

pg.quit()
