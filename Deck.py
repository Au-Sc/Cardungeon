import Game_Resources
import Game_Objects
from pygame import image
import Cards

class Deck(Game_Objects.Rectangular_Game_object):

    card_backside_img = Game_Resources.get_texture("Card_backside")
    
    def __init__(self, i_card_amount):
        super().__init__(10,30, Deck.card_backside_img.get_width(), Deck.card_backside_img.get_height())
        self.card_amount = i_card_amount
        Game_Resources.game_deck = self

    def draw_card(self):
        if(self.card_amount > 0):
            card = Cards.Enemy_Card(0,0,Game_Resources.get_texture("Skeleton"),1)
            self.card_amount -= 1
            return card
        else:
            return None

    def Draw(self, canvas):
        text = Game_Resources.main_font.render(str(self.card_amount),True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.center = (self.get_center_global())
        canvas.blit(Deck.card_backside_img, (self.x, self.y))
        canvas.blit(text,text_rect)

    def Update(self, deltatime):
        pass
