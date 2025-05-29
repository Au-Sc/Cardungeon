import Game_Objects
import Game_Resources
import pygame
import Cards

class Player(Game_Objects.GameObject):

    inventory_max_items = 7
    inventory_offset = (5,10)
    # inventory_offset[0] is offset between cards in inventory
    # inventory_offset[1] is separation between cards and bottom of the canvas
    inventory_rise_offset = 10
    
    def __init__(self, i_game, i_health):
        super().__init__(i_game,0,0)
        self.max_health = i_health
        self.health = i_health
        self.inventory = list()
        self.selected_item = None
        i_game.game_state.player = self

    def add_item(self, weapon: Cards.Card):
        if not (self.is_inventory_full()):
            self.inventory.append(weapon)
            self.reposition_items()

    def reposition_items(self):
        amount = len(self.inventory)
        width = self.game.get_texture("Card").get_width()
        height = self.game.get_texture("Card").get_height()
        left_offset = ( amount * width + (amount-1) * (Player.inventory_offset[0]) ) /2
        i = 0
        for item in self.inventory:
            item.x = (Game_Resources.CANVAS_WIDTH/2) - left_offset + i*(width + Player.inventory_offset[0])
            item.y = Game_Resources.CANVAS_HEIGHT - height - Player.inventory_offset[1]
            if (item is self.selected_item):
                item.y -= Player.inventory_rise_offset
            i += 1

    def select_item(self, item: Cards.Card):
        if (item.uses > 0):
            self.deselect_item()    
            self.selected_item = item
            item.y -= Player.inventory_rise_offset

    def deselect_item(self):
        if (self.selected_item != None):
            self.selected_item.y += Player.inventory_rise_offset
        self.selected_item = None

    def is_inventory_full(self):
        if (len(self.inventory) >= Player.inventory_max_items):
            return True
        return False

    def remove_item(self, item: Cards.ItemCard):
        if (item in self.inventory):
            self.inventory.remove(item)
            self.reposition_items()

    def action_tick(self):
        all_weapons_loaded = True
        for item in self.inventory:
            item.action_tick()
            if(item.uses == 0):
                all_weapons_loaded = False
        
        available = self.check_attack_availability()
        if not (available):
            if not (all_weapons_loaded):
                self.game.game_state.board.action_tick()
                self.action_tick()
                print("No moves available, reloading weapons.")
            else:
                print("No moves available at all, you've been defeated.")
                self.health = 0
            

    def get_attacked(self, amount: int):
        damage = amount
        for item in self.inventory:
            if(isinstance(item,Cards.ConsumableCard)):
                if(item.effect == Cards.ConsumableCard.PROTECT):
                    damage = 0
                    item.use()
                    break
        
        self.health -= damage
        if(self.health <= 0):
            self.health = 0

    def get_healed(self, amount: int):
        self.health += amount
        if (self.health > self.max_health):
            self.health = self.max_health

    def check_attack_availability(self):
        available = False
        if(self.game.game_state.board != None):
            checks = set()
            for item in self.inventory:
                if (isinstance(item, Cards.WeaponCard)) and (item.uses > 0):
                    checks.add((item.element,item.shape,item.melee))
            for x in range(self.game.game_state.board.COLUMNS):
                for y in range(self.game.game_state.board.ROWS):
                    for check in checks:
                        if (y == self.game.game_state.board.ROWS - 1) or not (check[2]):
                            if (Cards.WeaponTypes.validate_element_status(check[0],self.game.game_state.board.get(x,y).status)):
                                offsets = Cards.WeaponShapes.get_offsets(check[1])
                                valid = True
                                for i in range(1,len(offsets)):
                                    pos = (x + offsets[i][0], y + offsets[i][1])
                                    if (self.game.game_state.board.is_within_range(pos[0],pos[1])):
                                        if not(Cards.WeaponTypes.validate_element_status(check[0],self.game.game_state.board.get(pos[0],pos[1]).status)):
                                            valid = False
                                            break
                                if (valid):
                                    available = True
                                    break
                    if (available):
                        break
                if (available):
                        break
        return available
    
    def update(self):
        for e in self.game.events:
            
            if e.type == pygame.MOUSEBUTTONDOWN :
                #check if a card in the board was clicked.
                center = self.game.game_state.board.get_cell_under_cursor()
                
                if (self.game.game_state.board.is_within_range(center[0],center[1])):
                    obj = self.game.game_state.board.get(center[0],center[1])
                    
                    if (center[1] == self.game.game_state.board.ROWS - 1):
                        
                        if (isinstance(obj,Cards.EnemyCard)) and (self.selected_item != None):
                            self.selected_item.attack(center)
                            
                        if (isinstance(obj,Cards.ItemCard)):
                            
                            if (obj.status == Cards.CardStatuses.NEUTRAL) and (len(self.inventory) < Player.inventory_max_items):
                                self.add_item(obj)
                                self.game.game_state.board.discard(obj)
                            else:
                                if(self.selected_item != None):
                                    self.selected_item.attack(center)
                    else:
                        
                        if(self.selected_item != None):
                            self.selected_item.attack(center)
                        
                #check if a card from inventory was clicked.
                for item in self.inventory:
                    
                    if (item.contains_point(self.game.mouse_pos)):
                        
                        if (item is self.selected_item):
                            self.deselect_item()
                        else:
                            
                            if(isinstance(item,Cards.ConsumableCard)):
                                if not (item.passive):
                                    item.use()
                                    
                            if(isinstance(item,Cards.WeaponCard)):
                                self.select_item(item)
        
        for item in self.inventory:
            item.update()
        
    def render(self):
        self.game.render_text_to_display_centered(f"{self.health}/{self.max_health}",(100,Game_Resources.DISPLAY_HEIGHT - 150), (255,0,0,255), 60)
        
        for item in self.inventory:
            item.render()
