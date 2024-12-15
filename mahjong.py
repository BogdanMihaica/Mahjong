import pygame as pg
import random
pg.init()

# Board Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

GREEN = (44, 87, 36)
WHITE = (227, 227, 227)
GRAY = (50, 50, 50)
BLUE=(81, 94, 158)
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

def draw_piece(x_offset,y_offset,img):
            shadow_rect = pg.Rect(x_offset + 6, y_offset + 6, tile_size[0], tile_size[1])
            pg.draw.rect(window, GRAY, shadow_rect)
            border_rect = pg.Rect(x_offset+4, y_offset+4, tile_size[0], tile_size[1])
            pg.draw.rect(window, BLUE, border_rect, 2)

            border_rect = pg.Rect(x_offset+3, y_offset+3, tile_size[0], tile_size[1])
            pg.draw.rect(window, BLUE, border_rect, 2)
            
            border_rect = pg.Rect(x_offset+2, y_offset+2, tile_size[0], tile_size[1])
            pg.draw.rect(window, WHITE, border_rect, 2)

            border_rect = pg.Rect(x_offset+1, y_offset+1, tile_size[0], tile_size[1])
            pg.draw.rect(window, WHITE, border_rect, 2)
           
            window.blit(img, (x_offset, y_offset))




#shuffling cards
all_cards=[]
# values={
#      "stick":1,
#      "character":2,
#      "dot":3,
#      "dragon":
# }
for key in pieces:
     iterations=4
     
     if key=="flower" or key=="season":
          iterations=2
     for _ in range(iterations):
         for key1 in pieces[key]:
              all_cards.append({key1:pieces[key][key1]})

def display_pieces(all_cards,y_offset=20):
    x_offset = 20
    spacing = 10
    for card in all_cards:
        for name, img in card.items():
            draw_piece(x_offset, y_offset, img)
            x_offset += tile_size[0] + spacing
            if x_offset + tile_size[0] > SCREEN_WIDTH:
                x_offset = 20
                y_offset += tile_size[1] + spacing
random.shuffle(all_cards)
player1 = all_cards[0:13]
player2 = all_cards[13:26]
player3 = all_cards[26:39]
player4 = all_cards[39:52]
run = True
while run:
    window.blit(bg_image, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    display_pieces(player1)
    display_pieces(player2,80)
    display_pieces(player3,140)
    display_pieces(player4,200)

    pg.display.update()

pg.quit()
