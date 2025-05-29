import Game_Objects
import Game_Resources
import pygame
import enum
import random
from abc import abstractmethod


class Card(Game_Objects.RectangularGameObject):

    def __init__(self, i_game, i_x, i_y, i_content_img):
        self.card_img = i_game.get_texture("Card")
        super().__init__(i_game, i_x, i_y, self.card_img.get_width(), self.card_img.get_height())
        self.content_img = i_content_img
        self.content_img_width = i_content_img.get_width()
        self.content_img_height = i_content_img.get_height()
        self.status = CardStatuses.NEUTRAL

    @abstractmethod
    def action_tick(self):
        pass

    def clear_status(self):
        self.status = CardStatuses.NEUTRAL
        self.card_img = self.game.get_texture("Card")

    def set_status(self, status: int):
        if(status == CardStatuses.BURNING):
            self.status = CardStatuses.BURNING
            self.card_img = self.game.get_texture("Card_burning")
        
        if(status == CardStatuses.FROZEN):
            self.status = CardStatuses.FROZEN
            self.card_img = self.game.get_texture("Card_frozen")
        

    def render(self):
        center = self.get_center_global()
        content_pos = (center[0] - (self.content_img_width/2), center[1] - (self.content_img_height/2))
        
        self.game.canvas.blit(self.card_img,(self.x, self.y))
        self.game.canvas.blit(self.content_img, content_pos)

    @abstractmethod
    def update(self):
        pass


class CardStatuses(enum.Enum):
    NEUTRAL = 0
    BURNING = 1
    FROZEN = 2


class EnemyCard(Card):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_health: int, i_attack_cooldown: int, i_damage: int):
        super().__init__(i_game, i_x, i_y, i_content_img)
        self.health = i_health
        self.attack_cooldown = i_attack_cooldown
        self.attack_cooldown_ticks = i_attack_cooldown
        self.damage = i_damage
        self.flinch = False

    def get_attacked(self, damage: int):
        self.health -= damage
        self.flinch = True
        if self.health <= 0:
                self.die()

    def action_tick(self):
        if not self.flinch:
            if (self.attack_cooldown_ticks > 1):
                self.attack_cooldown_ticks -= 1
            else:
                if (self.attack_cooldown >= 0):
                    self.attack()
                    self.attack_cooldown_ticks = self.attack_cooldown
        else:
            self.flinch = False

    def attack(self):
        self.game.game_state.player.get_attacked(self.damage)
    
    def die(self):
        if (self.game.game_state.board != None) and (self.game.game_state.deck != None):
            self.game.game_state.deck.increase_item_weight()
            self.game.game_state.board.discard(self)
            self.game.remove_game_object(self)

    def update(self):
        pass
        
    def render(self):
        super().render()
        
        heart_img = self.game.get_texture("Heart_icon")
        offset = self.width/(self.health + 1)
        for x in range(self.health):
            self.game.canvas.blit(heart_img, (self.x + (x+1)*offset - heart_img.get_width()/2,self.y))

        if(self.attack_cooldown >= 0):
            pos = self.get_center_global()
            pos = (pos[0], pos[1]+15)
            text_pos = self.game.scale_to_display_size(pos)
            self.game.render_text_to_display_centered(str(self.attack_cooldown_ticks),text_pos,(255,255,255,255),30)

            pos = (pos[0] - 10, pos[1])
            text_pos = self.game.scale_to_display_size(pos)
            self.game.render_text_to_display_centered(str(self.damage),text_pos,(255,0,0,255),30)


class WeaponShapes():
    
    SINGLE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    CROSS = 3
    EX = 4
    
    SINGLE_OFFSETS = [(0,0)]
    HORIZONTAL_OFFSETS = [(0,0),(1,0),(-1,0)]
    VERTICAL_OFFSETS = [(0,0),(0,-1),(0,1)]
    CROSS_OFFSETS = [(0,0),(0,-1),(1,0),(0,1),(-1,0)]
    EX_OFFSETS = [(0,0),(1,-1),(1,1),(-1,1),(-1,-1)]
    
    def get_offsets(shape):
        if(shape == WeaponShapes.SINGLE):
            return WeaponShapes.SINGLE_OFFSETS
        if(shape == WeaponShapes.HORIZONTAL):
            return WeaponShapes.HORIZONTAL_OFFSETS
        if(shape == WeaponShapes.VERTICAL):
            return WeaponShapes.VERTICAL_OFFSETS
        if(shape == WeaponShapes.CROSS):
            return WeaponShapes.CROSS_OFFSETS
        if(shape == WeaponShapes.EX):
            return WeaponShapes.EX_OFFSETS


class WeaponTypes(enum.Enum):
    NEUTRAL = 0
    FIRE = 1
    ICE = 2

    def validate_element_status(element: int, status: int):
        if (status == CardStatuses.NEUTRAL):
            return True

        if (status == CardStatuses.BURNING) and (element == WeaponTypes.ICE):
            return True

        if (status == CardStatuses.FROZEN) and (element == WeaponTypes.FIRE):
            return True

        return False


class ItemCard(Card):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_uses):
        super().__init__(i_game, i_x, i_y, i_content_img)
        self.max_uses = i_uses
        self.uses = i_uses

    def render(self):
        super().render()
        if(self.uses > 0):
            used_height = (self.height/self.max_uses) * (self.max_uses - self.uses)
            used_y = self.y + self.height - used_height
            pygame.draw.rect(self.game.canvas,(230,230,230,255),[self.x, used_y, self.width, used_height])


class ConsumableCard(ItemCard):
    #EFFECTS:
    HEAL = 0
    PROTECT = 1
    
    def __init__(self, i_game, i_x, i_y, i_content_img, i_uses, i_effect, i_passive):
        super().__init__(i_game, i_x, i_y, i_content_img, i_uses)
        self.effect = i_effect
        self.passive = i_passive

    def use(self):
        if (self.game.game_state.player != None):

            if (self.effect == ConsumableCard.HEAL):
                amount = int(self.game.game_state.player.max_health // 5)
                self.game.game_state.player.get_healed(amount)
            
            self.uses -= 1
            if(self.uses < 1):
                self.game.game_state.player.remove_item(self)
                self.game.remove_game_object(self)

    def action_tick(self):
        pass

    def update(self):
        pass

    def render(self):
        super().render()
        

class WeaponCard(ItemCard):
    def __init__(self, i_game, i_x, i_y, i_content_img, i_uses : int, i_weaponshape : int, i_melee : bool, i_element : int, i_damage: int, i_cooldown : int):
        super().__init__(i_game, i_x, i_y, i_content_img, i_uses)
        self.used = False
        self.shape = i_weaponshape
        self.melee = i_melee
        self.damage = i_damage
        self.element = i_element
        self.cooldown = i_cooldown
        self.cooldown_ticks = 0

    def start_cooldown(self):
        self.cooldown_ticks = self.cooldown

    def action_tick(self):
        if (self.used):
            self.used = False
        else:
            if (self.cooldown_ticks > 0):
                self.cooldown_ticks -= 1
                if (self.cooldown_ticks == 0):
                    self.uses = self.max_uses

    def get_targets(self, center: (int,int)):
        targets = list()
        offsets = WeaponShapes.get_offsets(self.shape)
        for offset in offsets:
            pos = (center[0]+offset[0],center[1]+offset[1])
            if (self.game.game_state.board.is_within_range(pos[0],pos[1])):
                targets.append(self.game.game_state.board.get(pos[0],pos[1]))
        return targets

    def attack(self, center: (int,int)):
        if (self.game.game_state.player != None) and (self.game.game_state.board != None):
            if (center[1] == self.game.game_state.board.ROWS -1) or not (self.melee):
                if (self.uses > 0):
                    targets = self.get_targets(center)
                    can_attack = True
                    for t in targets:
                        if not(WeaponTypes.validate_element_status( self.element, t.status)):
                            can_attack = False
                    if(can_attack):
                        self.used = True
                        self.uses -= 1
                        for t in targets:
                            if(isinstance(t,EnemyCard)):
                                t.get_attacked(self.damage)
                                t.clear_status()
                            if(isinstance(t,ItemCard)):
                                if(t.status != CardStatuses.NEUTRAL):
                                    t.clear_status()
                                else:
                                    self.game.game_state.board.discard(t)
                        if (self.uses == 0):
                            self.start_cooldown()
                            self.game.game_state.player.deselect_item()
                        self.game.game_state.board.action_tick()
                        self.game.game_state.player.action_tick()

    def update(self):
        pass
        
    def render(self):
        super().render()

        element_rect = pygame.Rect(self.x,self.y,self.width,5)
        color = (200,200,200)
        if (self.element == WeaponTypes.FIRE):
            color = (250,150,100)
            
        if (self.element == WeaponTypes.ICE):
            color = (100,200,250)
                
        pygame.draw.rect(self.game.canvas,color,element_rect)
        
        if (self.game.game_state.player != None) and (self.game.game_state.board != None):
            if (self is self.game.game_state.player.selected_item):
                center = self.game.game_state.board.get_cell_under_cursor()
                if(center != (-1,-1)):
                    targets = self.get_targets(center)
                    for t in targets:
                        color = (255,255,255)
                        if (not (WeaponTypes.validate_element_status(self.element,t.status)) or
                            (self.melee and (center[1] != (self.game.game_state.board.ROWS - 1)))):
                            color = (255,0,0)
                        rect = t.card_img.get_rect()
                        rect.topleft = (t.x,t.y)
                        pygame.draw.rect(self.game.canvas,color,rect,3)

        if (self.uses == 0):
            cooldown_height = self.height * (self.cooldown_ticks/self.cooldown)
            cooldown_y = self.y + self.height - cooldown_height
            pygame.draw.rect(self.game.canvas,(70,70,70,255),[self.x, cooldown_y, self.width, cooldown_height])

                        
                        
