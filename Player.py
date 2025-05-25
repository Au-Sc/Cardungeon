import Game_Objects
import Game_Resources
import pygame
import Cards

class Player(Game_Objects.GameObject):
    def __init__(self, game):
        super().__init__(game,0,0)
        self.health = 50
        self.game.player = self
    
    def attack(self, enemy):
        if isinstance(enemy, Cards.EnemyCard):
            enemy.get_attacked(1)

    def get_attacked(self, damage: int):
        self.health -= damage
        if(self.health <= 0):
            self.health = 0
            self.defeat()

    def defeat(self):
        pass
    
    def update(self):
        for e in self.game.events:
            if e.type == pygame.MOUSEBUTTONDOWN :
                untouched = list()
                acted = False
                for x in range(self.game.board.COLUMNS):
                    for y in range(self.game.board.ROWS):
                        obj = self.game.board.get(x,y)
                        if isinstance(obj, Cards.EnemyCard):
                            if obj.contains_point(self.game.mouse_pos):
                                self.attack(obj)
                                acted = True
                            else:
                                untouched.append(obj)
                if (acted):
                    for e in untouched:
                        e.attack_tick()
        
    def render(self):
        h_text = self.game.big_font.render(str(self.health),True,(255,0,0))
        h_rect = h_text.get_rect()
        h_rect.midleft = (20,Game_Resources.DISPLAY_HEIGHT - 40)
        self.game.text_canvas.blit(h_text, h_rect)
