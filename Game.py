import pygame
from sys import exit
import Cards
import math

Canvas_Width = 800
Canvas_Height = 600

skeleton_img = pygame.image.load("sprites/skeleton.png")
card = Cards.Card(skeleton_img,Canvas_Width/2,Canvas_Height/2);

card.hscale = 3
card.vscale = 3

pygame.init()
window = pygame.display.set_mode((Canvas_Width, Canvas_Height))
pygame.display.set_caption("Cardungeon")

def Draw():
    window.fill((20,20,20))

    card.Draw(window)

    pygame.display.update()

elapsed = 0.0

Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    elapsed += 0.0015

    card.x = Canvas_Width/2 + ((Canvas_Width/4)*math.sin(2*elapsed))
    card.hscale = 3 + (2*math.sin(elapsed))
    card.vscale = card.hscale
    
    Draw()

pygame.quit()
