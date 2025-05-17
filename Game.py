import pygame
from sys import exit
import Cards
import math
import Board

Display_Width = 800
Display_Height = 600

Canvas_Width = 282
Canvas_Height = (Canvas_Width/4)*3

skeleton_img = pygame.image.load("sprites/Skeleton.png")
#card = Cards.Card(skeleton_img,Canvas_Width/2,Canvas_Height/2)

board = Board.Card_Board(4, 3)
for x in range(board.WIDTH):
    for y in range(board.HEIGHT):
        board.put(x, y, Cards.Card(skeleton_img, 72 + x*(Cards.Card.card_width + 10), 40 + y*(Cards.Card.card_height + 10)))

#card.hscale = 3
#card.vscale = 3

pygame.init()
window = pygame.display.set_mode((Display_Width, Display_Height))
canvas = pygame.Surface((Canvas_Width, Canvas_Height))
pygame.display.set_caption("Cardungeon")

def Draw():
    window.fill((20,20,20))

    #card.Draw(canvas)
    board.Draw(canvas)
    
    scaled_canvas = pygame.transform.scale(canvas,(Display_Width, Display_Height))
    window.blit(scaled_canvas,(0,0))
    pygame.display.update()

#elapsed = 0.0

Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

#    elapsed += 0.0015

#    card.x = Canvas_Width/2 + ((Canvas_Width/4)*math.sin(2*elapsed))
#    card.hscale = 3 + (2*math.sin(elapsed))
#    card.vscale = card.hscale
    
    Draw()

pygame.quit()
