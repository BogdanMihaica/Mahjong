import pygame as pg
import random
import socket
import threading
import pickle
#Socket configuration
HOST = "127.0.0.1"
PORT = 65432

# Game start
gameStarted=False
player=0
playerCards=[]

tile_size = (36, 50)
def load_image(path, size):
        try:
            img = pg.image.load(path)
            return pg.transform.scale(img, size)
        except FileNotFoundError:
            print(f"Error: File not found {path}")
            return pg.Surface(size)
        
def transform_cards(cards):
    crs=[]
    for card in cards:
        key=list(card.keys())[0]
        val=card[key]
        crs.append({key:load_image(val,tile_size)})
    return crs
def handle_wait(conn):
    global gameStarted,playerCards
    while not gameStarted:
        try:
            data = conn.recv(1024)
            if int(data):
                #if data == b"started":
                    player=int(data)
                    print(player)
                    toSend = b"ready"
                    conn.sendall(toSend)
                    gameStarted = True
                    #sending cards to players 
                    card_data = conn.recv(4096)  
                    cards = pickle.loads(card_data)
                    playerCards=transform_cards(cards)
                    print(playerCards)
                    
        except Exception as e:
            print(f"Some exception occurred: {e}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
        
    pg.init()
    pg.display.set_caption("Mahjong")
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

    values = {
        "stick_1": 1, "stick_2": 2, "stick_3": 3, "stick_4": 4, "stick_5": 5, "stick_6": 6, "stick_7": 7, "stick_8": 8, "stick_9": 9,
        "dot_1": 10, "dot_2": 11, "dot_3": 12, "dot_4": 13, "dot_5": 14, "dot_6": 15, "dot_7": 16, "dot_8": 17, "dot_9": 18,
        "character_1": 19, "character_2": 20, "character_3": 21, "character_4": 22, "character_5": 23, "character_6": 24, "character_7": 25, "character_8": 26, "character_9": 27,
        "dragon_1": 28, "dragon_2": 29, "dragon_3": 30,
        "wind_1": 32, "wind_2": 33, "wind_3": 34, "wind_4": 35,
        "flower_1": 36, "flower_2": 36, "flower_3": 36, "flower_4": 36,
        "season_1": 36, "season_2": 36, "season_3": 36, "season_4": 36
    }



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

    def text(x, y, fontsize, message, color=(255,255,255)):
        font = pg.font.SysFont("timesnewroman", fontsize)
        rendered_text = font.render(message, True, color)
        text_rect = rendered_text.get_rect(center=(x, y))
        window.blit(rendered_text, text_rect)

    def display_draw_area():
        surfaceW,surfaceH=200, 200
        x,y=150,SCREEN_HEIGHT//2-surfaceH//2-100
        surface=pg.Surface((surfaceW,surfaceH), pg.SRCALPHA)
        color=(0,255,0,70)
        surface.fill(color)
        border_color = (0, 255, 0)
        border_thickness = 5
        pg.draw.rect(surface, border_color, surface.get_rect(), border_thickness)
        window.blit(surface, (x,y))
        text_x = x+surfaceW//2
        text_y = y+surfaceH//2
        text(text_x, text_y, 30, "Draw card",color=(0, 255, 0))
        return pg.Rect(x,y,surfaceW,surfaceH)
    def display_discard_button():
        surfaceW,surfaceH=200, 80
        x,y=150,SCREEN_HEIGHT//2-surfaceH//2+150+10-100
        surface=pg.Surface((surfaceW,surfaceH), pg.SRCALPHA)
        color=(255,0,0,70)
        surface.fill(color)
        border_color = (255, 0, 0)
        border_thickness = 5
        pg.draw.rect(surface, border_color, surface.get_rect(), border_thickness)
        window.blit(surface, (x,y))
        text_x = x+surfaceW//2
        text_y = y+surfaceH//2
        text(text_x, text_y, 30, "Discard",color=(255, 0,0))
        return pg.Rect(x,y,surfaceW,surfaceH)
    def display_pick_last_button():
        surfaceW,surfaceH=200, 80
        x,y=150,SCREEN_HEIGHT//2-surfaceH//2+150+10
        surface=pg.Surface((surfaceW,surfaceH), pg.SRCALPHA)
        color=(0,0,255,70)
        surface.fill(color)
        border_color = (0, 0, 255)
        border_thickness = 5
        pg.draw.rect(surface, border_color, surface.get_rect(), border_thickness)
        window.blit(surface, (x,y))
        text_x = x+surfaceW//2
        text_y = y+surfaceH//2
        text(text_x, text_y, 20, "Pick last card",color=(255, 255, 255))
        return pg.Rect(x,y,surfaceW,surfaceH)
    def display_exposed_areas():
        padX=20
        s1h=SCREEN_HEIGHT-40
        s1w=tile_size[1]
        surface=pg.Surface((s1w,s1h), pg.SRCALPHA)
        color=(255,255,255,70)
        surface.fill(color)
        x,y=padX,20
        window.blit(surface, (x,y))
        x,y=SCREEN_WIDTH - padX -tile_size[1],20
        window.blit(surface, (x,y))

        s2h=tile_size[1]
        s2w=SCREEN_HEIGHT-40
        surface=pg.Surface((s2w,s2h), pg.SRCALPHA)
        color=(255,255,255,70)
        surface.fill(color)
        x,y=(SCREEN_WIDTH-s2w)//2,padX
        window.blit(surface, (x,y))
        x,y=(SCREEN_WIDTH-s2w)//2,SCREEN_HEIGHT-padX-tile_size[1]
        window.blit(surface, (x,y))
        return

    def handle_draw_card(cardsLeft, turn):
        return

    threading.Thread(target=handle_wait, args=(s,), daemon=True).start()
    run = True
    holdingCard=False
    heldCard=0
    heldCardIndex=0
    heldCardX=0
    heldCardY=0
   
    pickSound = pg.mixer.Sound("sounds/pick.wav")
   
    while run:
        draw=None
        discard=None
        pick=None
        window.blit(bg_image, (0, 0))
        if gameStarted==False:
             text(500,350,50,"Waiting for players")
        else:
            draw=display_draw_area()
            discard=display_discard_button()
            pick=display_pick_last_button()
            display_exposed_areas()
            x_offset, _ = center_pieces(playerCards, SCREEN_WIDTH, "horizontal")
            player1_rects = display_pieces(playerCards, x_offset, SCREEN_HEIGHT - tile_size[1] - 80, "horizontal", rotation=0)

            # Draw the highlight rectangle if holding a card
            if holdingCard:
                select_color = (255, 253, 117)
                card_action(heldCardX, heldCardY, select_color)

            # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and gameStarted==True:
                mouse_pos = pg.mouse.get_pos()
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
                if draw.collidepoint(mouse_pos):
                    print("Drew")
        pg.display.update()

    pg.quit()
