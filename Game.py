import pygame
import Game_Resources
import Game_Objects
from sys import exit
import Cards
import Board
import Deck
import Player


class Game():
    
    def __init__(self):
        #GAME ATRIBUTES AND VARIABLES BELOW
        self.RUNNING = False
        self.delta_time = 0
        self.game_objects = list()
        self.events = list()
        self.mouse_pos = (0,0)

        #TEXT ASSETS
        pygame.font.init()
        self.main_font = pygame.font.Font('freesansbold.ttf',15)

        #SPRITE ASSETS
        self.textures = dict()
        
        #GAME OBJECTS BELOW
        self.board = Board.Card_board(self, 4, 3)
        self.board.x = 52
        self.board.y = 0
        for cols in range(self.board.COLUMNS):
            for rows in range(self.board.ROWS):
                c = Cards.Enemy_Card(self, 0, 0, self.get_texture("Skeleton"), 1)
                self.board.put(cols, rows, c)
                
        self.player = Player.Player(self)
        self.deck = Deck.Deck(self, 20)
        self.blotch = [(255, 0, 0), (0, 0), 3, 0]
        
        #START GAME WINDOW BELOW
        pygame.init()
        self.window = pygame.display.set_mode((Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
        self.canvas = pygame.Surface((Game_Resources.CANVAS_WIDTH, Game_Resources.CANVAS_HEIGHT))
        pygame.display.set_caption("Cardungeon")
    
    def get_texture(self, name: str):
        texture = self.textures.get(name, None)

        if texture is None:
            return self.load_texture(name)
        else:
            return texture

    def load_texture(self, name: str):
        pathstr = f"sprites/{name}.png"
        texture = pygame.image.load(pathstr)
        self.textures[name] = texture
        return texture
        
    def add_game_object(self, obj): 
        if not (obj in self.game_objects):
            self.game_objects.append(obj)

    def remove_game_object(self, obj): 
        if (obj in self.game_objects):
            self.game_objects.remove(obj)

    def run(self):
        #START GAME FPS MANAGEMENT STUFF
        TARGET_TIME = (1000/60) #(milliseconds / frames) proportion
        last_time = pygame.time.get_ticks()
        self.delta_time = 0
        
        #START GAME LOOP
        self.RUNNING = True
        
        while self.RUNNING:
            now = pygame.time.get_ticks()
            self.delta_time += now - last_time
            
            if(self.delta_time >= TARGET_TIME):
                self.update()
                self.render()
                self.delta_time = 0
            
            last_time = now
        
        pygame.quit()

    def update(self):
        #catch the player input first.
        self.events = pygame.event.get()

        for e in self.events:
            if e.type == pygame.MOUSEMOTION:
                self.blotch[1] = e.pos
                self.mouse_pos = (e.pos[0] * Game_Resources.CANVAStoDISPLAY_width_ratio,
                                  e.pos[1] * Game_Resources.CANVAStoDISPLAY_height_ratio)
            if e.type == pygame.QUIT:
                self.RUNNING = False
        
        #now update the game.
        for obj in self.game_objects:
            obj.update()
        
    def render(self):
        self.window.fill((20,20,20))
        
        for obj in self.game_objects:
            obj.render()
        
        scaled_canvas = pygame.transform.scale(self.canvas,(Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
        self.window.blit(scaled_canvas,(0,0))
        
        pygame.draw.circle(self.window, self.blotch[0], self.blotch[1], self.blotch[2], self.blotch[3])
        
        pygame.display.update()
        self.canvas.fill((0,0,0))


#RUN THE GAME!!
game = Game()
game.run()
