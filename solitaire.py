"""
Solitaire Card Game
Evan Mead - University of Vermont
CS021
"""
import pygame
import random
import csv
import datetime

DISPLAY_CARD_SIZE = (50, 70)

# setup function || shuffles the deck, deals the table, and sets up click boxes
def setup():
    random.shuffle(full_deck)
    for i in range(7):
        for j in range(i+1):
            table[i].append(full_deck.pop())
        random.shuffle(table[i])
        table[i][-1].active = True
    for i in range(7):
        empty_boxes.append(pygame.Rect(70+(i*60), 10, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1]))
        
# update function || called continuously, draws elements to the screen
def update():
    pygame.display.flip()
    screen.fill(COLOR)

    if full_deck:
        for i in range(5):
            screen.blit(card_back, (10, (i * -5) + 30))
    else:
        screen.blit(empty, (10, 10))

    if hand:
        for x in range(len(hand)):
            hand[x].x = 10
            hand[x].y = (x * 20) + 120
            hand[x].c_box = pygame.Rect(hand[x].x, hand[x].y, 50, 18)
            hand[x].draw(hand[x].x + hand[x].disp[0], hand[x].y + hand[x].disp[1])
        hand[-1].c_box = pygame.Rect(hand[-1].x, hand[-1].y, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])
    else:
        screen.blit(empty, (10, 120))

    for x in range(len(table)):
        if table[x]:
            for y in range(len(table[x])):
                table[x][y].x = 70 + (x * 60)
                table[x][y].y = 10 + (y * 18)
                table[x][y].draw(table[x][y].x + table[x][y].disp[0], table[x][y].y + table[x][y].disp[1])
                table[x][y].c_box = pygame.Rect(table[x][y].x, table[x][y].y, 50, 18)
            table[x][-1].c_box = pygame.Rect(table[x][-1].x, table[x][-1].y, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])
        else:
            screen.blit(empty, (70 + (x * 60), 10))

    screen.blit(hearts_spot, (500, 10))
    screen.blit(diamonds_spot, (500, 90))
    screen.blit(clubs_spot, (500, 170))
    screen.blit(spades_spot, (500, 250))

    for i in range(4):
        if storage[i]:
            for x in storage[i]:
                x.draw(500, 10 + (i * 80))

# draw cards function || pulls 'x' cards from the deck and into hand, if nothing in deck it flips the hand into the deck
def draw_cards():
    if hand:
        for _ in range(len(hand)):
            drawn_deck.append(hand.pop())
    for i in range(cards_to_flip):
        if full_deck:
            hand.append(full_deck.pop())
            hand[i].active = True
    if not(full_deck):
        for i in range(len(drawn_deck)):
            full_deck.append(drawn_deck.pop())
    
# card hover funciton || purely graphical, responsible for "highlighting" the card the pointer is "hovering" over
def card_hover():
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j].active == True:
                if (table[i][j].c_box).collidepoint(pygame.mouse.get_pos()):
                    table[i][j].disp = [10, 0]
                    table[i][j].draw(table[i][j].x + table[i][j].disp[0], table[i][j].y + table[i][j].disp[1])
                else:
                    table[i][j].disp = [0, 0]
    
    if(hearts_box.collidepoint(pygame.mouse.get_pos())):
        screen.blit(highlight, (500, 10))
    if(diamonds_box.collidepoint(pygame.mouse.get_pos())):
        screen.blit(highlight, (500, 90))
    if(clubs_box.collidepoint(pygame.mouse.get_pos())):
        screen.blit(highlight, (500, 170))
    if(spades_box.collidepoint(pygame.mouse.get_pos())):
        screen.blit(highlight, (500, 250))
    
    for i in range(len(hand)):
        if (hand[i].c_box).collidepoint(pygame.mouse.get_pos()):
            hand[i].disp = [10, 0]
            hand[i].draw(hand[i].x + hand[i].disp[0], hand[i].y + hand[i].disp[1])
        else:
            hand[i].disp = [0, 0]
    
    for i in selected:
        if i[0] != "":
            i[0].disp = [10, 0]

# stack function || validates that the card being added to a stack is exactly 1 less than the previous and of the opposite color
def stack(bottom, top):
    b_val = 0
    t_val = 0
    try:
        b_val = int(bottom.number)
    except ValueError:
        if bottom.number == "a":
            b_val = 1
        if bottom.number == "j":
            b_val = 11
        if bottom.number == "q":
            b_val = 12
        if bottom.number == "k":
            b_val = 13
    try:
        t_val = int(top.number)
    except ValueError:
        if top.number == "a":
            t_val = 1
        if top.number == "j":
            t_val = 11
        if top.number == "q":
            t_val = 12
        if top.number == "k":
            t_val = 13
    if t_val == b_val + 1:
        return True
    else:
        return False

# switch function || moves card elements and their children between stacks
def switch():
    if selected[0][1] == "hand":
        if selected[0][0] == hand[-1]:
            if selected[1][1] == "table":
                if stack(selected[0][0], selected[1][0]):
                    if selected[0][0].color != selected[1][0].color:
                        table[selected[1][2]].append(selected[0][0])
                        table[selected[1][2]][-1].disp = [0, 0]
                        table[selected[1][2]][-1].disp = [0, 0]
                        hand.pop()
            elif selected[1][1] == "hearts" and selected[0][0].suit == "h":
                if selected[0][0].number == "a":
                    storage[0].append(hand.pop())
                else:
                    if storage[0]:
                        if stack(storage[0][-1], selected[0][0]):
                            storage[0].append(hand.pop())
            elif selected[1][1] == "diamonds" and selected[0][0].suit == "d":
                if selected[0][0].number == "a":
                    storage[1].append(hand.pop())
                else:
                    if storage[1]:
                        if stack(storage[1][-1], selected[0][0]):
                            storage[1].append(hand.pop())
            elif selected[1][1] == "clubs" and selected[0][0].suit == "c":
                if selected[0][0].number == "a":
                    storage[2].append(hand.pop())
                else:
                    if storage[2]:
                        if stack(storage[2][-1], selected[0][0]):
                            storage[2].append(hand.pop())
            elif selected[1][1] == "spades" and selected[0][0].suit == "s":
                if selected[0][0].number == "a":
                    storage[3].append(hand.pop())
                else:
                    if storage[3]:
                        if stack(storage[3][-1], selected[0][0]):
                            storage[3].append(hand.pop())
            for i in range(7):
                if selected[1][1] == str(i):
                    if selected[0][0].number == "k":
                        table[int(selected[1][1])].append(hand.pop())

    elif selected[0][1] == "table":
        card_in_stack = len(table[selected[0][2]]) - selected[0][3]

        if selected[1][0] != "":
            if stack(selected[0][0], selected[1][0]):
                if selected[0][0].color != selected[1][0].color:
                    for i in range(card_in_stack):
                        table[selected[1][2]].append(table[selected[0][2]].pop(selected[0][3]))

        if selected[1][1] == "hearts" and selected[0][0].suit == "h":
            if selected[0][0].number == "a":
                storage[0].append(table[selected[0][2]].pop())
            else:
                if storage[0]:
                    if stack(storage[0][-1], selected[0][0]):
                        storage[0].append(table[selected[0][2]].pop())
        elif selected[1][1] == "diamonds" and selected[0][0].suit == "d":
            if selected[0][0].number == "a":
                storage[1].append(table[selected[0][2]].pop())
            else:
                if storage[1]:
                    if stack(storage[1][-1], selected[0][0]):
                        storage[1].append(table[selected[0][2]].pop())
        elif selected[1][1] == "clubs" and selected[0][0].suit == "c":
            if selected[0][0].number == "a":
                storage[2].append(table[selected[0][2]].pop())
            else:
                if storage[2]:
                    if stack(storage[2][-1], selected[0][0]):
                        storage[2].append(table[selected[0][2]].pop())
        elif selected[1][1] == "spades" and selected[0][0].suit == "s":
            if selected[0][0].number == "a":
                storage[3].append(table[selected[0][2]].pop())
            else:
                if storage[3]:
                    if stack(storage[3][-1], selected[0][0]):
                        storage[3].append(table[selected[0][2]].pop()) 

        for i in range(7):
            if selected[1][1] == str(i):
                if selected[0][0].number == "k":
                    for i in range(card_in_stack):
                        table[int(selected[1][1])].append(table[selected[0][2]].pop(selected[0][3]))

    for i in range(len(table)):
        if table[i]:
            table[i][-1].active = True

def check_solved():
    counts = 0
    for x in table:
        if x:
            for y in x:
                if y.active == False:
                    counts += 1
    return counts

# Card Class || Defines carcds and their properties such as position, suit, color, and value
class Card:
    def __init__(self, suit, number, color, x, y, c_box, active, disp):
        self.suit = suit
        self.number = number
        self.color = color
        self.x = x
        self.y = y
        self.c_box = c_box
        self.active = active
        self.disp = disp

    def __str__(self):
        return(f"{self.number}{self.suit}")

    def draw(self, x, y):
        if self.active == True:
            screen.blit(CARD_IMAGES[f"{self.number}{self.suit}"], (x, y))
        else:
            screen.blit(card_back, (x, y))


if __name__ == "__main__":

    full_deck = []
    suits = ["h", "c", "s", "d"]
    colors = ["R", "B", "B", "R"]
    
    table = [[], [], [], [], [], [], []]
    hand = []
    selected = []
    storage = [[], [], [], []]
    drawn_deck = []

    COLOR = (48, 43, 42)
    WINDOW_WIDTH = 560
    WINDOW_HEIGHT = 360

    CARD_IMAGES = {}
    INDICATORS = {}

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('Solitaire')  
    card_back = pygame.image.load("sprites/card_back.png")
    draw_box = pygame.Rect(10, 10, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])

    highlight = pygame.image.load("sprites/highlight.png")
    empty = pygame.image.load("sprites/empty.png")

    hearts_spot = pygame.image.load("sprites/hearts_spot.png")
    hearts_box = pygame.Rect(500, 10, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])
    diamonds_spot = pygame.image.load("sprites/diamonds_spot.png")
    diamonds_box = pygame.Rect(500, 90, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])
    clubs_spot = pygame.image.load("sprites/clubs_spot.png")
    clubs_box = pygame.Rect(500, 170, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])
    spades_spot = pygame.image.load("sprites/spades_slot.png")
    spades_box = pygame.Rect(500, 250, DISPLAY_CARD_SIZE[0], DISPLAY_CARD_SIZE[1])

    empty_boxes = []
    cards_to_flip = 0
    win_state = False
    moves = 0

    with open("launch_settings.txt") as f:
        data = f.readlines()
        cards_to_flip = int(data[0].strip("\n"))
        card_back = pygame.image.load(data[1].strip("\n"))

    running = True
    turn = "player"

    for i in range(4):
        for j in range(1, 10):
            full_deck.append(Card(suits[i], str(j+1), colors[i], 0, 0, pygame.Rect(0, 0, 0, 0), False, [0, 0]))
            CARD_IMAGES[str(full_deck[-1])] = pygame.image.load(f"sprites/52/{str(full_deck[-1])}.png")
        full_deck.append(Card(suits[i], "j", colors[i], 0, 0, pygame.Rect(0, 0, 0, 0), False, [0, 0]))
        CARD_IMAGES[str(full_deck[-1])] = pygame.image.load(f"sprites/52/{str(full_deck[-1])}.png")
        full_deck.append(Card(suits[i], "q", colors[i], 0, 0, pygame.Rect(0, 0, 0, 0), False, [0, 0]))
        CARD_IMAGES[str(full_deck[-1])] = pygame.image.load(f"sprites/52/{str(full_deck[-1])}.png")
        full_deck.append(Card(suits[i], "k", colors[i], 0, 0, pygame.Rect(0, 0, 0, 0), False, [0, 0]))
        CARD_IMAGES[str(full_deck[-1])] = pygame.image.load(f"sprites/52/{str(full_deck[-1])}.png")
        full_deck.append(Card(suits[i], "a", colors[i], 0, 0, pygame.Rect(0, 0, 0, 0), False, [0, 0]))
        CARD_IMAGES[str(full_deck[-1])] = pygame.image.load(f"sprites/52/{str(full_deck[-1])}.png")

    setup()
    while running:
        update()
        card_hover()

        if len(selected) == 2:
            switch()
            if selected[0] != selected[1]:
                moves += 1
                print(f"Moves: {moves}")
                if check_solved() == 0 and not(hand) and not(full_deck) and not(drawn_deck):
                    print(f"Deck Solved with {moves} moves.")
                    with open("log.csv", "a") as f:
                        write = csv.writer(f)
                        write.writerow([datetime.datetime.now(), "Solved", moves])
                        f.close()
                    exit()
            selected = []
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if draw_box.collidepoint(pygame.mouse.get_pos()):
                    draw_cards()
                for x in range(len(table)):
                    for y in range(len(table[x])):
                        if table[x][y].c_box.collidepoint(pygame.mouse.get_pos()):
                            if table[x][y].active == True:
                                selected.append((table[x][y], "table", x, y))
                for i in range(len(hand)):
                    if hand[i].c_box.collidepoint(pygame.mouse.get_pos()):
                        selected.append((hand[i], "hand"))
                if hearts_box.collidepoint(pygame.mouse.get_pos()):
                    selected.append(("", "hearts"))
                elif diamonds_box.collidepoint(pygame.mouse.get_pos()):
                    selected.append(("", "diamonds"))
                elif spades_box.collidepoint(pygame.mouse.get_pos()):
                    selected.append(("", "spades"))
                elif clubs_box.collidepoint(pygame.mouse.get_pos()):
                    selected.append(("", "clubs"))
                for x, i in enumerate(empty_boxes):
                    if not(table[x]):
                        if i.collidepoint(pygame.mouse.get_pos()):
                            selected.append(("", str(x)))