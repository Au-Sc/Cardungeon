import pygame
import Game_Resources
from sys import exit
import Game_Objects
import Game_States


class Game():
    
    def __init__(self):
        #GAME ATRIBUTES AND VARIABLES BELOW
        self.RUNNING = False
        self.delta_time = 0
        self.game_objects = list()
        self.events = list()
        self.mouse_pos = (0,0)
        self.blotch = [(255, 0, 0), (0, 0), 3, 0]
        self.game_state = None

        #TEXT ASSETS
        pygame.font.init()
        self.small_font = pygame.font.Font('./fonts/autobahn_2/Autobahn.ttf',30)
        self.big_font = pygame.font.Font('./fonts/autobahn_2/Autobahn.ttf',60)
        self.huge_font = pygame.font.Font('./fonts/autobahn_2/Autobahn.ttf',60)
        
        #START GAME WINDOW BELOW
        pygame.init()
        self.window = pygame.display.set_mode((Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
        self.canvas = pygame.Surface((Game_Resources.CANVAS_WIDTH, Game_Resources.CANVAS_HEIGHT), pygame.SRCALPHA)
        self.text_canvas = pygame.Surface((Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT), pygame.SRCALPHA)
        pygame.display.set_caption("Cardungeon")

    def change_state(self, state : Game_States.GameState):
        self.game_state = state
        if not (self.game_state.started):
            self.game_state.start()
    
    def get_texture(self, name: str):
        if(self.game_state != None):
            texture = self.game_state.textures.get(name, None)
            
            if texture is None:
                return self.load_texture(name)
            else:
                return texture

    def load_texture(self, name: str):
        pathstr = f"sprites/{name}.png"
        texture = pygame.image.load(pathstr)
        self.game_state.textures[name] = texture
        return texture
        
    def add_game_object(self, obj): 
        if not (obj in self.game_objects):
            self.game_objects.append(obj)

    def remove_game_object(self, obj): 
        if (obj in self.game_objects):
            self.game_objects.remove(obj)

    def scale_to_display_size(self, pos: (float,float)):
        return (pos[0]*Game_Resources.DtoC_w_ratio, pos[1]*Game_Resources.DtoC_h_ratio)

    def scale_to_canvas_size(self, pos: (float,float)):
        return (pos[0]*Game_Resources.CtoD_w_ratio, pos[1]*Game_Resources.CtoD_h_ratio)

    def render_text_to_display_centered(self, text: str, center: (float,float), color, size = 30):
        font = self.big_font
        if(size == 30):
            font = self.small_font
        if (size == 120):
            font = self.huge_font
        
        rendered_text = font.render(text,True,color)
        pos = (center[0] - (rendered_text.get_width()/2), center[1] - (rendered_text.get_height()/2))
        self.text_canvas.blit(rendered_text, pos)

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
                self.mouse_pos = self.scale_to_canvas_size(e.pos)
            if e.type == pygame.QUIT:
                self.RUNNING = False
                
        if(self.game_state != None):
            self.game_state.update()
        
    def render(self):
        self.window.fill((25,25,25))
        self.canvas.fill((0,0,0,0))
        self.text_canvas.fill((0,0,0,0))

        if(self.game_state != None):
            self.game_state.render()
        
        scaled_canvas = pygame.transform.scale(self.canvas,(Game_Resources.DISPLAY_WIDTH, Game_Resources.DISPLAY_HEIGHT))
        self.window.blit(scaled_canvas,(0,0))
        self.window.blit(self.text_canvas,(0,0))
        
        pygame.draw.circle(self.window, self.blotch[0], self.blotch[1], self.blotch[2], self.blotch[3])
        
        pygame.display.update()


#RUN THE GAME!!
game = Game()
game.change_state(Game_States.MainMenuState(game))
game.run()
