from pygame import image
from pygame import transform

class Card:

    card_img = image.load("sprites/Card.png")
    card_width = card_img.get_width()
    card_height = card_img.get_height()
    
    def __init__(self, i_content_img, i_x, i_y):
        self.content_img = i_content_img
        self.x = i_x
        self.y = i_y
        self.width = i_content_img.get_width()
        self.height = i_content_img.get_height()
        self.hscale = 1
        self.vscale = 1

    def Draw(self, canvas):
        scaled_cardw = Card.card_width * self.hscale
        scaled_cardh = Card.card_height * self.vscale
        scaled_w = self.width * self.hscale
        scaled_h = self.height * self.vscale
        
        cardf_x = self.x - (scaled_cardw/2)
        cardf_y = self.y - (scaled_cardh/2) 
        f_x = self.x - (scaled_w/2)
        f_y = self.y - (scaled_h/2)

        scaled_card_img = transform.scale(Card.card_img,(scaled_cardw,scaled_cardh))
        scaled_content_img = transform.scale(self.content_img, (scaled_w,scaled_h))

        canvas.blit(scaled_card_img,(cardf_x,cardf_y))
        canvas.blit(scaled_content_img,(f_x,f_y))
        
