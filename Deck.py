import Game_Objects
import Cards

class Deck(Game_Objects.RectangularGameObject):
    
    def __init__(self, i_game, i_card_amount):
        self.backside_img = i_game.get_texture("Card_backside")
        super().__init__(i_game,10,30, self.backside_img.get_width(), self.backside_img.get_height())
        self.card_amount = i_card_amount
        self.game.deck = self

    def draw_card(self):
        if(self.card_amount > 0):
            card = Cards.Enemy_Card(self.game, 0, 0, self.game.get_texture("Skeleton"), 2)
            self.game.add_game_object(card)
            self.card_amount -= 1
            return card
        else:
            return None

    def render(self):
        text = self.game.main_font.render(str(self.card_amount),True,(255,255,255))
        text_rect = text.get_rect()
        text_rect.center = (self.get_center_global())
        self.game.canvas.blit(self.backside_img, (self.x, self.y))
        self.game.canvas.blit(text,text_rect)

    def update(self):
        pass
