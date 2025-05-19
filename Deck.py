import Game_Objects
from pygame import image, font

font.init()

class Deck(Game_Objects.Rectangular_Game_object):

    card_backside_img = image.load("sprites/Card_backside.png")
    count_font = font.Font('freesansbold.ttf',15)
    
    def __init__(self, i_card_amount):
        super().__init__(10,30, Deck.card_backside_img.get_width(), Deck.card_backside_img.get_height())
        self.card_amount = i_card_amount

    def Draw(self, canvas):
        text = Deck.count_font.render(str(self.card_amount),True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.center = (self.get_center_global())
        canvas.blit(Deck.card_backside_img, (self.x, self.y))
        canvas.blit(text,text_rect)

    def Update(self, game_data, deltatime):
        pass
