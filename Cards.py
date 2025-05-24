import Game_Objects
import pygame
from abc import abstractmethod

class Card(Game_Objects.RectangularGameObject):

    Card_id = 0

    def __init__(self, i_game, i_x, i_y, i_content_img):
        self.card_img = i_game.get_texture("Card")
        super().__init__(i_game, i_x, i_y, self.card_img.get_width(), self.card_img.get_height())
        self.content_img = i_content_img
        self.content_img_width = i_content_img.get_width()
        self.content_img_height = i_content_img.get_height()
        self.id = Card.Card_id
        Card.Card_id += 1

    def render(self):
        center = self.get_center_global()
        content_pos = (center[0] - (self.content_img_width/2), center[1] - (self.content_img_height/2))
        
        self.game.canvas.blit(self.card_img,(self.x, self.y))
        self.game.canvas.blit(self.content_img, content_pos)
        
        text = self.game.main_font.render(str(self.id),True,(0,255,0))
        text_rect = text.get_rect()
        text_rect.center = (center)
        self.game.canvas.blit(text,text_rect)

    @abstractmethod
    def update(self):
        pass

class Enemy_Card(Card):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_health: int):
        super().__init__(i_game, i_x, i_y, i_content_img)
        self.health = i_health

    def get_attacked(self, damage: int):
        self.health -= damage
        if self.health <= 0:
                self.die()
    
    def die(self):
        if self.game.board != None:
            self.game.board.discard(self)
            self.game.remove_game_object(self)

    def update(self):
        pass
        
    def render(self):
        super().render()
        heart_img = self.game.get_texture("Heart_icon")
        offset = self.width/(self.health + 1)
        for x in range(self.health):
            self.game.canvas.blit(heart_img, (self.x + (x+1)*offset - heart_img.get_width()/2,self.y))
