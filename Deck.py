import Game_Resources
import Game_Objects
import Cards
import random

class Prototype():
    #types:
    ENEMY = 0
    WEAPON = 1
    CONSUMABLE = 2
    
    def __init__(self, i_type, i_name: str, i_weight: int):
        self.type = i_type
        self.NAME = i_name
        self.weight = i_weight
        self.settings = list()

#type should be one of the types declared in this class, indicates what class to instantiate
#name should be an understandable and unique name for the Prototype
#weight defines how likely it is for this prototype to be chosen.
#he average weight value is 200.
#maller values make it less likely to be chosen,
#bigger values make it more likely to be chosen.
#settings are the values needed to instantiate a particular version of the class from the prototype's type

class Deck(Game_Objects.RectangularGameObject):
    
    def __init__(self, i_game, i_card_amount):
        super().__init__(i_game,10,30, 0, 0)
        self.card_amount = i_card_amount
        self.enemy_pool = list()
        self.enemy_weight = 0
        self.item_pool = list()
        self.base_item_weight = 0
        self.item_weight = 0
        self.item_weight_increase = 0
        self.game.game_state.deck = self

    def increase_item_weight(self):
        self.item_weight += self.item_weight_increase

    def draw_card(self):

        card = None
        
        pool_weight = self.item_weight + self.enemy_weight
        chosen_weight = random.random() * pool_weight
        
        if (chosen_weight - self.item_weight <= 0):
            self.item_weight = self.base_item_weight
            pool_weight = 0
            for p in self.item_pool:
                pool_weight += p.weight

            chosen_weight = random.random() * pool_weight
            chosen = None
            
            for p in self.item_pool:
                chosen_weight -= p.weight
                if(chosen_weight <= 0):
                    chosen = p
                    if(p.type == Prototype.WEAPON):
                        self.item_pool.remove(p)
                    break
            
            if (p.type == Prototype.WEAPON):
                card = Cards.WeaponCard(self.game, 0, 0, self.game.get_texture(chosen.settings[0]),
                                        chosen.settings[1], chosen.settings[2], chosen.settings[3],
                                        chosen.settings[4], chosen.settings[5], chosen.settings[6])
                card.set_status(chosen.settings[7])
                
            if (p.type == Prototype.CONSUMABLE):
                card = Cards.ConsumableCard(self.game, 0, 0, self.game.get_texture(chosen.settings[0]),
                                            chosen.settings[1], chosen.settings[2], chosen.settings[3])
                card.set_status(chosen.settings[4])
        else:
            pool_weight = 0
            for p in self.enemy_pool:
                pool_weight += p.weight

            chosen_weight = random.random() * pool_weight
            chosen = None
        
            for p in self.enemy_pool:
                chosen_weight -= p.weight
                if(chosen_weight <= 0):
                    chosen = p
                    break
                
            card = Cards.EnemyCard(self.game, 0, 0, self.game.get_texture(chosen.settings[0]), chosen.settings[1],
                                   chosen.settings[2], chosen.settings[3])
            card.set_status(chosen.settings[4])
            
        if (self.card_amount > 0):
            self.card_amount -= 1
        
        return card

    def render(self):

        remaining_cards_text = f"defeat {self.card_amount}"
        if (self.card_amount > 1):
            remaining_cards_text += " enemies to go !!"
        if (self.card_amount == 1):
            remaining_cards_text += " enemy to go !!"
        
        self.game.render_text_to_display_centered(remaining_cards_text,(Game_Resources.DISPLAY_WIDTH/2,30),(255,255,255,255),30)

    def update(self):
        pass
