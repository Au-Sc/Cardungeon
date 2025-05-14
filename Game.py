import pygame
from sys import exit

Canvas_Width = 800
Canvas_Height = 600

card_img = pygame.image.load("sprites/skeleton.png")

pygame.init()
window = pygame.display.set_mode((Canvas_Width, Canvas_Height))
pygame.display.set_caption("Cardungeon")

def Draw():
    window.fill((20,20,20))
    window.blit(card_img,(Canvas_Width/2,Canvas_Height/2))
    pygame.display.update()

Running = True

while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = false

    Draw()
pygame.quit()
