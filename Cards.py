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

class EnemyCard(Card):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_health: int):
        super().__init__(i_game, i_x, i_y, i_content_img)
        self.health = i_health
        self.attack_cooldown = 3

    def get_attacked(self, damage: int):
        self.health -= damage
        if self.health <= 0:
                self.die()

    def attack_tick(self):
        if (self.attack_cooldown > 1):
            self.attack_cooldown -= 1
        else:
            self.game.player.get_attacked(1)
            self.attack_cooldown = 3
    
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
            
        attack_in = self.game.small_font.render(str(self.attack_cooldown),True,(255,50,50))
        attack_rect = attack_in.get_rect()
        pos = self.get_center_global()
        pos = (pos[0], pos[1]+15)
        pos = self.game.scale_to_display_size(pos)
        attack_rect.center = pos
        self.game.text_canvas.blit(attack_in, attack_rect)

class WeaponCard(Card):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_weaponshape, i_damage):
        super().__init__(i_game, i_x, i_y, i_content_img)
        self.shape = i_weaponshape
        self.damage = i_damage
