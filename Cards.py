import Game_Resources
import Game_Objects
from pygame import image
from pygame import transform
from pygame import Rect
from abc import abstractmethod

class Card(Game_Objects.Rectangular_Game_object):

    card_img = Game_Resources.get_texture("Card")
    Card_id = 0

    def __init__(self, i_x, i_y, i_content_img):
        w = Card.card_img.get_width()
        h = Card.card_img.get_height()
        super().__init__(i_x, i_y, w, h)
        self.content_img = i_content_img
        self.content_img_width = i_content_img.get_width()
        self.content_img_height = i_content_img.get_height()
        self.id = Card.Card_id
        Card.Card_id += 1

    def Draw(self, canvas):
        center = self.get_center_global()
        content_pos = (center[0] - (self.content_img_width/2), center[1] - (self.content_img_height/2))
        
        canvas.blit(Card.card_img,(self.x, self.y))
        canvas.blit(self.content_img,content_pos)
        
        text = Game_Resources.main_font.render(str(self.id),True,(0,255,0))
        text_rect = text.get_rect()
        text_rect.center = (center)
        canvas.blit(text,text_rect)

    @abstractmethod
    def Update(self, deltatime):
        pass

class Enemy_Card(Card):
    def __init__(self, i_x, i_y, i_content_img, i_health: int):
        super().__init__(i_x, i_y, i_content_img)
        self.health = i_health

    def get_attacked(self, damage: int):
        self.health -= damage

        if(self.health <= 0):
            self.die()
    
    def die(self):
        if(Game_Resources.game_board != None):
            pos = Game_Resources.game_board.find_card(self)
            if (pos != (-1,-1)):
                Game_Resources.game_board.pop(pos[0],pos[1])
                Game_Resources.remove_game_object(self)
                Game_Resources.game_board.refill()

    def Update(self, deltatime):
        pass

    def Draw(self, canvas):
        super().Draw(canvas)
        heart_img = Game_Resources.get_texture("Heart_icon")
        offset = self.width/(self.health + 1)
        for x in range(self.health):
            canvas.blit(heart_img, (self.x + (x+1)*offset - heart_img.get_width()/2,self.y))
