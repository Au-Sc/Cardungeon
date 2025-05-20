import pygame
import Game_Resources
import Game_Objects
from sys import exit
import Cards
import Board
import Deck
import Player

#GAMEPLAY TESTING VARIABLES // MUST BE DELETED AT THE FINAL VERSION, THESE ARE ONLY TO TEST STUFF AROUND AND DEBUG
board = Board.Card_board(4, 3)
player = Player.Player()

board.x = 52
board.y = 40
for cols in range(board.COLUMNS):
    for rows in range(board.ROWS):
        c = Cards.Enemy_Card(0, 0, Game_Resources.get_texture("Skeleton"), 1)
        board.put(cols, rows, c)

deck = Deck.Deck(20)
blotch = [(255,0,0),(0,0),3,0]


#END OF GAMEPLAY TESTING VARIABLES SECTION // REMEMBER TO DELETE AT THE FINAL VERSION, THESE ARE ONLY TO TEST STUFF AROUND AND DEBUG


#DEFINE INPUT READING STATE OF THE GAME LOOP
def Read_Input(events):
    #resetting some input previously received
    Game_Resources.mouse_button_down = False
    Game_Resources.mouse_button_up = False
    
    #receiving new input
    for e in events:
        if e.type == pygame.QUIT:
            Game_Resources.RUNNING = False
            
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1:
                Game_Resources.mouse_button_down = True
                Game_Resources.mouse_button_helddown = True

        
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                Game_Resources.mouse_button_up = True
                Game_Resources.mouse_button_helddown = False

        
        if e.type == pygame.MOUSEMOTION:
            Game_Resources.mouse_pos = (e.pos[0]*Game_Resources.CANVAStoDISPLAY_width_ratio,e.pos[1]*Game_Resources.CANVAStoDISPLAY_height_ratio)


#DEFINE UPDATING STATE OF THE GAME LOOP
def Game_Loop_Update(deltatime):
    for obj in Game_Resources.game_objects:
        obj.Update(deltatime)

#DEFINE DRAWING STATE OF THE GAME LOOP
def Game_Loop_Draw():
    Window.fill((20,20,20))

    for obj in Game_Resources.game_objects:
        obj.Draw(canvas)
    
    pygame.draw.circle(canvas,blotch[0],Game_Resources.mouse_pos,blotch[2],blotch[3])
    
    scaled_canvas = pygame.transform.scale(canvas,(Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
    Window.blit(scaled_canvas,(0,0))
    
    pygame.display.update()
    canvas.fill((0,0,0))


#START GAME WINDOW
pygame.init()
Window = pygame.display.set_mode((Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
canvas = pygame.Surface((Game_Resources.CANVAS_WIDTH, Game_Resources.CANVAS_HEIGHT))
pygame.display.set_caption("Cardungeon")

#START GAME FPS MANAGEMENT STUFF
Last_time = pygame.time.get_ticks()
Delta_time = 0
Target_time = (1000/60) #(milliseconds / frames) proportion

#START GAME LOOP

Game_Resources.RUNNING = True

while Game_Resources.RUNNING:

    now = pygame.time.get_ticks()
    Delta_time += now - Last_time
    
    if(Delta_time >= Target_time):
        Read_Input(pygame.event.get())
        Game_Loop_Update(Delta_time)
        Game_Loop_Draw()
        Delta_time = 0

    Last_time = now

pygame.quit()
