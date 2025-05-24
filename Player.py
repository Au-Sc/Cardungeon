import Game_Objects
import pygame
import Cards

class Player(Game_Objects.GameObject):
    def __init__(self, game):
        super().__init__(game,0,0)
        self.game.player = self
    
    def attack(self, enemy):
        if isinstance(enemy, Cards.Enemy_Card):
            enemy.get_attacked(1)
    
    def update(self):
        for e in self.game.events:
            if e.type == pygame.MOUSEBUTTONDOWN :
                for x in range(self.game.board.COLUMNS):
                    for y in range(self.game.board.ROWS):
                        obj = self.game.board.get(x,y)
                        if isinstance(obj, Cards.Enemy_Card):
                            if obj.contains_point(self.game.mouse_pos):
                                self.attack(obj)
                                break
        
    def render(self):
        pass
