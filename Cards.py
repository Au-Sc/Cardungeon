import Game_Resources
import Game_Objects
from pygame import image
from pygame import transform
from pygame import Rect

class Card((Game_Objects.Rectangular_Game_object)):

    card_img = Game_Resources.get_texture("Card")
    
    def __init__(self, i_x, i_y, i_content_img):
        w = Card.card_img.get_width()
        h = Card.card_img.get_height()
        super().__init__(i_x, i_y, w, h)
        self.content_img = i_content_img
        self.content_img_width = i_content_img.get_width()
        self.content_img_height = i_content_img.get_height()
        self.visible = True

    def Draw(self, canvas):
        if not(self.visible):
            return
        
        center = self.get_center_global()
        content_pos = (center[0] - (self.content_img_width/2), center[1] - (self.content_img_height/2))

        canvas.blit(Card.card_img,(self.x, self.y))
        canvas.blit(self.content_img,content_pos)
        
    def Update(self, deltatime):
        pass
        #if Game_Resources.mouse_button_down and self.contains_point(Game_Resources.mouse_pos):
         #       self.visible = not self.visible
