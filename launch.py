import pygame

def update():
    pygame.display.flip()
    screen.blit(backdrop, (0, 0))

    screen.blit(standard, (280, 160))
    screen.blit(python, (360, 160))
    screen.blit(uvm, (440, 160))
    screen.blit(draw_1, (120, 150))
    screen.blit(draw_3, (120, 210))

    screen.blit(play_type, (220, 270))

    if selected_card_type == "sprites/card_back.png":
        screen.blit(selected, (278, 158))
    elif selected_card_type == "sprites/python_back.png":
        screen.blit(selected, (358, 158))
    elif selected_card_type == "sprites/uvm_back.png":
        screen.blit(selected, (438, 158))

    if standard_box.collidepoint(pygame.mouse.get_pos()):
        screen.blit(highlight, (280, 160))
    if python_box.collidepoint(pygame.mouse.get_pos()):
        screen.blit(highlight, (360, 160))
    if uvm_box.collidepoint(pygame.mouse.get_pos()):
        screen.blit(highlight, (440, 160))

    if draw_selected == 1:
        screen.blit(card_selected, (118, 148))
    if draw_selected == 3:
        screen.blit(card_selected, (118, 208))

    if play_box.collidepoint(pygame.mouse.get_pos()):
        screen.blit(play2, (220, 270))

def close():
    with open("launch_settings.txt", "w") as f:
        f.write(f"{draw_selected}\n{selected_card_type}")
    exit()
    


runing = True

selected_card_type = ""
draw_selected = 0

backdrop = pygame.image.load("sprites/backdrop.png")
standard = pygame.image.load("sprites/card_display.png")
python = pygame.image.load("sprites/python_display.png")
uvm = pygame.image.load("sprites/uvm_display.png")
highlight = pygame.image.load("sprites/highlight_display.png")
selected = pygame.image.load("sprites/select.png")
card_selected = pygame.image.load("sprites/draw_select.png")
draw_1 = pygame.image.load("sprites/draw1.png")
draw_3 = pygame.image.load("sprites/draw3.png")
play1 = pygame.image.load("sprites/play1.png")
play2 = pygame.image.load("sprites/play2.png")

play_type = play1

standard_box = pygame.Rect(280, 150, 70, 90)
python_box = pygame.Rect(340, 150, 70, 90)
uvm_box = pygame.Rect(440, 150, 70, 90)

draw_1_box = pygame.Rect(120, 150, 150, 50)
draw_3_box = pygame.Rect(120, 210, 150, 50)

play_box = pygame.Rect(220, 270, 100, 50)

WINDOW_WIDTH = 560
WINDOW_HEIGHT = 360

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Solitaire')  

while runing:
    update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if standard_box.collidepoint(pygame.mouse.get_pos()):
                selected_card_type = "sprites/card_back.png"
            if python_box.collidepoint(pygame.mouse.get_pos()):
                selected_card_type = "sprites/python_back.png"
            if uvm_box.collidepoint(pygame.mouse.get_pos()):
                selected_card_type = "sprites/uvm_back.png"
            if draw_1_box.collidepoint(pygame.mouse.get_pos()):
                draw_selected = 1
            if draw_3_box.collidepoint(pygame.mouse.get_pos()):
                draw_selected = 3
            if play_box.collidepoint(pygame.mouse.get_pos()):
                close()