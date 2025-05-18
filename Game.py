import pygame
from sys import exit
import Cards
import math
import Board

#DEFINE IMORTANT INITIAL GAME ATTRIBUTES
class Game_data():
    RUNNING = False
    DISPLAY_WIDTH = 800
    DISPLAY_HEIGHT = 600

    CANVAS_WIDTH = 282
    CANVAS_HEIGHT = (CANVAS_WIDTH/4)*3

    mouse_pos = (0,0)
    mouse_button_down = False
    mouse_button_helddown = False
    mouse_button_up = False


#GAMEPLAY TESTING VARIABLES // MUST BE DELETED AT THE FINAL VERSION, THESE ARE ONLY TO TEST STUFF AROUND AND DEBUG
skeleton_img = pygame.image.load("sprites/Skeleton.png")

board = Board.Card_Board(4, 3)
for x in range(board.WIDTH):
    for y in range(board.HEIGHT):
        board.put(x, y, Cards.Card(skeleton_img, 72 + x*(Cards.Card.card_width + 10), 40 + y*(Cards.Card.card_height + 10)))

blotch = [(255,255,255),(0,0),30,0]
blotch2 = [(255,0,0),(0,0),10,0]


#END OF GAMEPLAY TESTING VARIABLES SECTION // REMEMBER TO DELETE AT THE FINAL VERSION, THESE ARE ONLY TO TEST STUFF AROUND AND DEBUG


#DEFINE INPUT READING STATE OF THE GAME LOOP
def Read_Input(events):
    #resetting some input previously received
    Game_data.mouse_button_down = False
    Game_data.mouse_button_up = False
    
    #receiving new input
    for e in events:
        if e.type == pygame.QUIT:
            Game_data.RUNNING = False
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                Game_data.mouse_button_down = True
                Game_data.mouse_button_helddown = True

        
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                Game_data.mouse_button_up = True
                Game_data.mouse_button_helddown = False

        
        if e.type == pygame.MOUSEMOTION:
            Game_data.mouse_pos = e.pos


#DEFINE UPDATING STATE OF THE GAME LOOP
def Game_Loop_Update(deltatime):

#DEFINE DRAWING STATE OF THE GAME LOOP
def Game_Loop_Draw():
    Window.fill((20,20,20))
    
    board.Draw(canvas)
    
    scaled_canvas = pygame.transform.scale(canvas,(Game_data.DISPLAY_WIDTH, Game_data.DISPLAY_HEIGHT))
    Window.blit(scaled_canvas,(0,0))
    
    pygame.display.update()
    canvas.fill((0,0,0))


#START GAME WINDOW
pygame.init()
Window = pygame.display.set_mode((Game_data.DISPLAY_WIDTH, Game_data.DISPLAY_HEIGHT))
canvas = pygame.Surface((Game_data.CANVAS_WIDTH, Game_data.CANVAS_HEIGHT))
pygame.display.set_caption("Cardungeon")

#START GAME FPS MANAGEMENT STUFF
Last_time = pygame.time.get_ticks()
Delta_time = 0
Target_time = (1000/60) #(milliseconds / frames) proportion

#START GAME LOOP

Game_data.RUNNING = True

while Game_data.RUNNING:

    now = pygame.time.get_ticks()
    Delta_time += now - Last_time
    
    if(Delta_time >= Target_time):
        Read_Input(pygame.event.get())
        Game_Loop_Update(0)
        Game_Loop_Draw()
        Delta_time = 0

    Last_time = now

pygame.quit()
