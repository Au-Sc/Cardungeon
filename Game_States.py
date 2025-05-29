import pygame
import Game_Resources
import Game_Objects
import Cards
import Board
import Deck
from Deck import Prototype
import Player


class Button(Game_Objects.RectangularGameObject):
    def __init__(self, i_game, i_pos: (float,float), i_size: (float,float), i_text: str, i_text_size):
        super().__init__(i_game, i_pos[0], i_pos[1], i_size[0], i_size[1])
        self.text = i_text
        self.text_size = i_text_size
        self.pressed = False

    def update(self):
        for e in self.game.events:
            if (e.type == pygame.MOUSEBUTTONDOWN):
                if self.contains_point(self.game.mouse_pos):
                    self.pressed = True

    def render(self):
        button_color = (150,150,150,255)
        text_color = (250,250,250,255)

        if(self.pressed):
            button_color = (50,50,50,255)
            text_color = (150,150,150,255)

        pygame.draw.rect(self.game.canvas, button_color, [self.x,self.y,self.width,self.height],0,5)
        
        pos = self.get_center_global()
        pos = self.game.scale_to_display_size(pos)
        self.game.render_text_to_display_centered(self.text, pos, text_color, self.text_size)
        

class GameState():
    def __init__(self, i_game):
        self.game = i_game
        self.textures = dict()
        self.started = False
    
    def start(self):
        pass

    def update(self):
        pass

    def render(self):
        pass


class LevelConfig:
    def __init__(self):
        self.player_max_health = 50
        self.player_weapons = list()
        self.card_amount = 50
        self.enemy_weight = 300
        self.enemy_pool = list()
        self.item_weight = 50
        self.item_weight_increase = 20
        self.item_pool = list()
        self.bg_color = (20,20,20,255)

#Enemy Prototype settings has:
#[0] texture name
#[1] health amount
#[2] attack cooldown (negative values means the enemy does not attacks at all)
#[3] attack damage
#[4] default status (from the ones enumerated in Cards.py CardStatuses class) 0 = NEUTRAL, 1 = BURNING, 2 = FROZEN
#Enemy Prototypes:

    skeleton = Prototype(Prototype.ENEMY, "skeleton", 200)
    skeleton.settings = ["Skeleton", 1, -1, 0, Cards.CardStatuses.NEUTRAL]
    
    angry_skeleton = Prototype(Prototype.ENEMY, "angry_Skeleton", 150)
    angry_skeleton.settings = ["Skeleton", 1, 2, 1, Cards.CardStatuses.NEUTRAL]
    
    slime = Prototype(Prototype.ENEMY, "slime", 50)
    slime.settings = ["Slime", 3, -1, 0, Cards.CardStatuses.NEUTRAL]
    
    werewolf = Prototype(Prototype.ENEMY, "werewolf", 50)
    werewolf.settings = ["Werewolf", 1, 3, 5, Cards.CardStatuses.NEUTRAL]

    frozen_skeleton = Prototype(Prototype.ENEMY, "frozen_Skeleton", 70)
    frozen_skeleton.settings = ["Skeleton", 1, 2, 1, Cards.CardStatuses.FROZEN]

    burning_skeleton = Prototype(Prototype.ENEMY, "burning_Skeleton", 70)
    burning_skeleton.settings = ["Skeleton", 1, 2, 1, Cards.CardStatuses.BURNING]

    walking_bomb = Prototype(Prototype.ENEMY, "walking_bomb", 50)
    walking_bomb.settings = ["Walking_bomb", 2, 5, 20, Cards.CardStatuses.NEUTRAL]

    slime_icy = Prototype(Prototype.ENEMY, "slime_icy", 50)
    slime_icy.settings = ["Slime_icy", 7, -1, 0, Cards.CardStatuses.FROZEN]

    slime_fiery = Prototype(Prototype.ENEMY, "slime_fiery", 50)
    slime_fiery.settings = ["Slime_fiery", 4, 5, 5, Cards.CardStatuses.BURNING]
    
    frozen_werewolf = Prototype(Prototype.ENEMY, "frozen_werewolf", 50)
    frozen_werewolf.settings = ["Werewolf", 3, 4, 5, Cards.CardStatuses.FROZEN]

    burning_walking_bomb = Prototype(Prototype.ENEMY, "burning_walking_bomb", 100)
    burning_walking_bomb.settings = ["Walking_bomb", 3, 7, 20, Cards.CardStatuses.NEUTRAL]

#Consumable Prototype settings has
#[0] texture name
#[1] uses
#[2] effect (from the ones enumerated in Cards.py ConsumableCard class) 0 = HEALING, 1 = PROTECT 
#[3] is it a passive consumable (True or False)
#[4] default status (from the ones enumerated in Cards.py CardStatuses class) 0 = NEUTRAL, 1 = BURNING, 2 = FROZEN
#consumable prototypes:
    health_potion = Prototype(Prototype.CONSUMABLE,"health_potion",20)
    health_potion.settings = ["Health_potion", 1, Cards.ConsumableCard.HEAL, False, Cards.CardStatuses.NEUTRAL]

    burning_health_potion = Prototype(Prototype.CONSUMABLE,"burning_health_potion",20)
    burning_health_potion.settings = ["Health_potion", 2, Cards.ConsumableCard.HEAL, False, Cards.CardStatuses.FROZEN]

    shield = Prototype(Prototype.CONSUMABLE,"shield",100)
    shield.settings = ["Shield", 3, Cards.ConsumableCard.PROTECT, True, Cards.CardStatuses.NEUTRAL]

    frozen_shield = Prototype(Prototype.CONSUMABLE,"frozen_shield",100)
    frozen_shield.settings = ["Shield", 5, Cards.ConsumableCard.PROTECT, True, Cards.CardStatuses.NEUTRAL]

#Weapon Prototype settings has
#[0] texture name
#[1] uses
#[2] weapon shape (from the ones enumerated in Cards.py WeaponShapes class)
#[3] if it is a melee weapon or not (True or False)
#[4] element of the weapon (from the ones enumerated in Cards.py WeaponTypes class)
#[5] damage it deals
#[6] cooldown, how many actions it takes for it to reload once its uses become 0
#[7] default status (from the ones enumerated in Cards.py CardStatuses class) 0 = NEUTRAL, 1 = BURNING, 2 = FROZEN
#weapon prototypes

    bow = Prototype(Prototype.WEAPON,"bow",100)
    bow.settings = ["Bow", 3, Cards.WeaponShapes.SINGLE, False,
                           Cards.WeaponTypes.NEUTRAL, 1, 2, Cards.CardStatuses.NEUTRAL]

    spear = Prototype(Prototype.WEAPON,"spear",100)
    spear.settings = ["Spear", 4, Cards.WeaponShapes.VERTICAL, True,
                           Cards.WeaponTypes.NEUTRAL, 1, 1, Cards.CardStatuses.NEUTRAL]

    staff = Prototype(Prototype.WEAPON,"staff",100)
    staff.settings = ["Staff", 1, Cards.WeaponShapes.CROSS, False, 
                           Cards.WeaponTypes.NEUTRAL, 3, 3, Cards.CardStatuses.NEUTRAL]
    
    fire_sword = Prototype(Prototype.WEAPON,"fire_sword",100)
    fire_sword.settings = ["Sword", 3, Cards.WeaponShapes.HORIZONTAL, True,
                           Cards.WeaponTypes.FIRE, 2, 2, Cards.CardStatuses.NEUTRAL]

    fire_bow = Prototype(Prototype.WEAPON,"fire_bow",100)
    fire_bow.settings = ["Bow", 3, Cards.WeaponShapes.SINGLE, False,
                           Cards.WeaponTypes.FIRE, 1, 2, Cards.CardStatuses.BURNING]

    ice_spear = Prototype(Prototype.WEAPON,"ice_spear",100)
    ice_spear.settings = ["Spear", 3, Cards.WeaponShapes.VERTICAL, True,
                           Cards.WeaponTypes.ICE, 2, 1, Cards.CardStatuses.NEUTRAL]

    ice_bow = Prototype(Prototype.WEAPON,"ice_bow",100)
    ice_bow.settings = ["Bow", 3, Cards.WeaponShapes.SINGLE, False,
                           Cards.WeaponTypes.ICE, 1, 2, Cards.CardStatuses.FROZEN]

    dagger = Prototype(Prototype.WEAPON,"dagger",70)
    dagger.settings = ["Dagger", 2, Cards.WeaponShapes.SINGLE, True,
                           Cards.WeaponTypes.NEUTRAL, 4, 1, Cards.CardStatuses.NEUTRAL]

    fire_staff = Prototype(Prototype.WEAPON,"fire_staff",40)
    fire_staff.settings = ["Staff", 1, Cards.WeaponShapes.CROSS, False, 
                           Cards.WeaponTypes.FIRE, 5, 4, Cards.CardStatuses.BURNING]

    ice_staff = Prototype(Prototype.WEAPON,"ice_staff",40)
    ice_staff.settings = ["Staff", 1, Cards.WeaponShapes.CROSS, False, 
                           Cards.WeaponTypes.ICE, 5, 4, Cards.CardStatuses.FROZEN]

    ice_sword = Prototype(Prototype.WEAPON,"ice_sword",100)
    ice_sword.settings = ["Sword", 3, Cards.WeaponShapes.HORIZONTAL, True,
                           Cards.WeaponTypes.ICE, 2, 2, Cards.CardStatuses.NEUTRAL]

    fire_spear = Prototype(Prototype.WEAPON,"fire_spear",100)
    fire_spear.settings = ["Spear", 3, Cards.WeaponShapes.VERTICAL, True,
                           Cards.WeaponTypes.FIRE, 2, 1, Cards.CardStatuses.NEUTRAL]

    fire_dagger = Prototype(Prototype.WEAPON,"fire_dagger",40)
    fire_dagger.settings = ["Dagger", 2, Cards.WeaponShapes.SINGLE, True,
                           Cards.WeaponTypes.FIRE, 6, 2, Cards.CardStatuses.BURNING]

    ice_dagger = Prototype(Prototype.WEAPON,"ice_dagger",40)
    ice_dagger.settings = ["Dagger", 2, Cards.WeaponShapes.SINGLE, True,
                           Cards.WeaponTypes.ICE, 6, 2, Cards.CardStatuses.FROZEN]

class PauseState(GameState):

    PAUSE = 0
    WIN = 1
    DEFEAT = 2
    
    def __init__(self, i_game, i_pause_type, i_previous_state: "PlayingState"):
        super().__init__(i_game)
        self.pause_type = i_pause_type
        self.previous_state = i_previous_state

    def start(self):
        self.started = True
        pos = (Game_Resources.CANVAS_WIDTH/3, Game_Resources.CANVAS_HEIGHT/2)
        pos = (pos[0],pos[1] + Game_Resources.CANVAS_HEIGHT/14)
        size = (Game_Resources.CANVAS_WIDTH/3, Game_Resources.CANVAS_HEIGHT/7)

        return_text = ""
        if (self.pause_type == PauseState.PAUSE):
            return_text = "Continue level"
        if (self.pause_type == PauseState.WIN):
            return_text = "Replay level"
        if (self.pause_type == PauseState.DEFEAT):
            return_text = "Retry level"
        
        self.return_button = Button(self.game, pos, size, return_text,30)

        pos = (pos[0],pos[1] + Game_Resources.CANVAS_HEIGHT*3/14)
        self.level_menu_button = Button(self.game, pos, size, "Back to level menu", 30)

    def update(self):
        self.return_button.update()
        self.level_menu_button.update()
        
        if (self.return_button.pressed):
            if (self.pause_type == PauseState.PAUSE):
                self.game.change_state(self.previous_state)
                
            if (self.pause_type == PauseState.WIN) or (self.pause_type == PauseState.DEFEAT):
                new_game = PlayingState(self.game)
                new_game.config = self.previous_state.config
                self.game.change_state(new_game)
            
        if (self.level_menu_button.pressed):
            self.game.change_state(LevelMenuState(self.game))

    def render(self):
        title = ""
        title_color = (250,250,250,255) 
        
        if (self.pause_type == PauseState.PAUSE):
            title = "PAUSE"
        if (self.pause_type == PauseState.WIN):
            title = "VICTORY"
            title_color = (255,255,0,255)
        if (self.pause_type == PauseState.DEFEAT):
            title = "DEFEAT"
            title_color = (255,0,0,255)

        pos = (Game_Resources.DISPLAY_WIDTH/2, Game_Resources.DISPLAY_HEIGHT/4)
        self.game.render_text_to_display_centered(title, pos, title_color, 120)

        self.return_button.render()
        self.level_menu_button.render()

    
class PlayingState(GameState):
    def __init__(self, i_game):
        super().__init__(i_game)
        self.config = None

    def start(self):
        self.started = True
        if(self.config != None):
            self.textures = dict()
            
            self.player = Player.Player(self.game, self.config.player_max_health)
            for w in self.config.player_weapons:
                copy = Cards.WeaponCard(self.game,0,0,w.content_img,w.uses,w.shape,w.melee,w.element,w.damage,w.cooldown)
                self.player.add_item(copy)
            
            self.deck = Deck.Deck(self.game, 100000)
            self.deck.enemy_weight = self.config.enemy_weight
            self.deck.enemy_pool = self.config.enemy_pool
            self.deck.base_item_weight = self.config.item_weight
            self.deck.item_weight = self.config.item_weight
            self.deck.item_weight_increase = self.config.item_weight_increase
            self.deck.item_pool = self.config.item_pool

            c_t = self.game.get_texture("Card")
            c_z = (c_t.get_width(),c_t.get_height())
            self.board = Board.Board(self.game, 5, 3, c_z)
            self.board.x = 55
            self.board.y = 20
            while(True):
                for cols in range(self.board.COLUMNS):
                    for rows in range(self.board.ROWS):
                        c = self.deck.draw_card()
                        self.board.put(cols, rows, c)
                if(self.player.check_attack_availability()):
                    break

            self.deck.card_amount = self.config.card_amount

    def update(self):
        for e in self.game.events:
            if (e.type == pygame.KEYDOWN):
                if (e.key == pygame.K_ESCAPE):
                    self.game.change_state(PauseState(self.game, PauseState.PAUSE, self))
        
        if(self.config != None):
            self.player.update()
            self.board.update()
            self.deck.update()

            if (self.player.health <= 0):
                self.game.change_state(PauseState(self.game, PauseState.DEFEAT, self))

            if (self.deck.card_amount <= 0):
                self.game.change_state(PauseState(self.game, PauseState.WIN, self))

    def render(self):
        if(self.config != None):
            self.game.canvas.fill(self.config.bg_color)
            self.board.render()
            self.deck.render()
            self.player.render()





class LevelMenuState(GameState):
    def __init__(self, i_game):
        super().__init__(i_game)

    def start(self):
        self.started = True
        size = (Game_Resources.CANVAS_WIDTH/4, Game_Resources.CANVAS_HEIGHT/12)

        pos = (Game_Resources.CANVAS_WIDTH*3/8, Game_Resources.CANVAS_HEIGHT*2/8)
        
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/24)
        self.level1_button = Button(self.game, pos, size, "Level 1",30)

        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/8)
        self.level2_button = Button(self.game, pos, size, "Level 2",30)
        
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/8)
        self.level3_button = Button(self.game, pos, size, "Level 3",30)
        
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/8)
        self.level4_button = Button(self.game, pos, size, "Level 4",30)
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/12)
        
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/16)
        self.main_menu_button = Button(self.game, pos, size, "Back",30)

    def update(self):
        self.level1_button.update()
        self.level2_button.update()
        self.level3_button.update()
        self.level4_button.update()
        self.main_menu_button.update()

        if (self.main_menu_button.pressed):
            self.game.change_state(MainMenuState(self.game))

        l_c = None
        
        if (self.level1_button.pressed):
            l_c = LevelConfig()
            l_c.bg_color = (50,50,150,255)
            l_c.player_max_health = 50
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.NEUTRAL, 1, 1))
            
            l_c.card_amount = 30
            l_c.enemy_weight = 300
            l_c.item_weight = 50
            l_c.item_weight_increase = 15
            
            p = list()
            p.append(LevelConfig.skeleton)
            p.append(LevelConfig.werewolf)
            p.append(LevelConfig.slime)
            l_c.enemy_pool = p

            p = list()
            p.append(LevelConfig.health_potion)
            p.append(LevelConfig.shield)
            p.append(LevelConfig.spear)
            p.append(LevelConfig.bow)
            p.append(LevelConfig.staff)
            l_c.item_pool = p

        if (self.level2_button.pressed):
            l_c = LevelConfig()
            l_c.bg_color = (50,150,50,255)
            l_c.player_max_health = 50
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.NEUTRAL, 1, 1))

            l_c.card_amount = 50
            l_c.enemy_weight = 300
            l_c.item_weight = 50
            l_c.item_weight_increase = 10
            
            p = list()
            p.append(LevelConfig.skeleton)
            p.append(LevelConfig.werewolf)
            p.append(LevelConfig.slime)
            p.append(LevelConfig.frozen_skeleton)
            p.append(LevelConfig.burning_skeleton)
            p.append(LevelConfig.walking_bomb)
            l_c.enemy_pool = p

            p = list()
            p.append(LevelConfig.health_potion)
            p.append(LevelConfig.shield)
            p.append(LevelConfig.spear)
            p.append(LevelConfig.bow)
            p.append(LevelConfig.staff)
            p.append(LevelConfig.fire_sword)
            p.append(LevelConfig.ice_spear)
            p.append(LevelConfig.fire_bow)
            p.append(LevelConfig.ice_bow)
            l_c.item_pool = p

        if (self.level3_button.pressed):
            l_c = LevelConfig()
            l_c.bg_color = (130,130,50,255)
            l_c.player_max_health = 70
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.FIRE, 2, 1))
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.ICE, 2, 1))
            
            l_c.card_amount = 70
            l_c.enemy_weight = 400
            l_c.item_weight = 50
            l_c.item_weight_increase = 10
            
            p = list()
            p.append(LevelConfig.skeleton)
            p.append(LevelConfig.werewolf)
            p.append(LevelConfig.slime)
            p.append(LevelConfig.frozen_skeleton)
            p.append(LevelConfig.burning_skeleton)
            p.append(LevelConfig.walking_bomb)
            p.append(LevelConfig.slime_icy)
            p.append(LevelConfig.slime_fiery)
            l_c.enemy_pool = p

            p = list()
            p.append(LevelConfig.health_potion)
            p.append(LevelConfig.shield)
            p.append(LevelConfig.spear)
            p.append(LevelConfig.bow)
            p.append(LevelConfig.staff)
            p.append(LevelConfig.fire_sword)
            p.append(LevelConfig.ice_spear)
            p.append(LevelConfig.fire_bow)
            p.append(LevelConfig.ice_bow)
            p.append(LevelConfig.dagger)
            p.append(LevelConfig.fire_staff)
            p.append(LevelConfig.ice_staff)
            p.append(LevelConfig.burning_health_potion)
            p.append(LevelConfig.frozen_shield)
            l_c.item_pool = p

        if (self.level4_button.pressed):
            l_c = LevelConfig()
            l_c.bg_color = (150,50,50,255)
            l_c.player_max_health = 70
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.FIRE, 2, 1))
            l_c.player_weapons.append(Cards.WeaponCard( self.game, 0, 0, self.game.get_texture("Sword"), 4, Cards.WeaponShapes.HORIZONTAL, True, Cards.WeaponTypes.ICE, 2, 1))
            
            l_c.card_amount = 100
            l_c.enemy_weight = 500
            l_c.item_weight = 50
            l_c.item_weight_increase = 10
            
            p = list()
            p.append(LevelConfig.skeleton)
            p.append(LevelConfig.werewolf)
            p.append(LevelConfig.slime)
            p.append(LevelConfig.frozen_skeleton)
            p.append(LevelConfig.burning_skeleton)
            p.append(LevelConfig.walking_bomb)
            p.append(LevelConfig.slime_icy)
            p.append(LevelConfig.slime_fiery)
            p.append(LevelConfig.frozen_werewolf)
            p.append(LevelConfig.burning_walking_bomb)
            l_c.enemy_pool = p

            p = list()
            p.append(LevelConfig.health_potion)
            p.append(LevelConfig.shield)
            p.append(LevelConfig.spear)
            p.append(LevelConfig.bow)
            p.append(LevelConfig.staff)
            p.append(LevelConfig.fire_sword)
            p.append(LevelConfig.ice_spear)
            p.append(LevelConfig.fire_bow)
            p.append(LevelConfig.ice_bow)
            p.append(LevelConfig.dagger)
            p.append(LevelConfig.fire_staff)
            p.append(LevelConfig.ice_staff)
            p.append(LevelConfig.burning_health_potion)
            p.append(LevelConfig.frozen_shield)
            p.append(LevelConfig.fire_dagger)
            p.append(LevelConfig.ice_dagger)
            p.append(LevelConfig.ice_sword)
            p.append(LevelConfig.fire_spear)
            l_c.item_pool = p

        if(l_c != None):
            new_game = PlayingState(self.game)
            new_game.config = l_c
            self.game.change_state(new_game)

    def render(self):
        pos = (Game_Resources.DISPLAY_WIDTH/2, Game_Resources.DISPLAY_HEIGHT/5)
        self.game.render_text_to_display_centered("Select a level", pos, (250,250,250,255), 60)

        self.level1_button.render()
        self.level2_button.render()
        self.level3_button.render()
        self.level4_button.render()
        self.main_menu_button.render()


class MainMenuState(GameState):
    def __init__(self, i_game):
        super().__init__(i_game)

    def start(self):
        self.started = True
        size = (Game_Resources.CANVAS_WIDTH/3,Game_Resources.CANVAS_HEIGHT/7)
        pos = (Game_Resources.CANVAS_WIDTH/3,Game_Resources.CANVAS_HEIGHT/2)
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT/14)
        self.play_button = Button(self.game, pos, size, "Play", 30)
        
        pos = (pos[0], pos[1] + Game_Resources.CANVAS_HEIGHT*3/14)
        self.quit_button = Button(self.game, pos, size, "Quit", 30)

    def update(self):
        self.play_button.update()
        self.quit_button.update()

        if (self.play_button.pressed):
            self.game.change_state(LevelMenuState(self.game))

        if (self.quit_button.pressed):
            self.game.RUNNING = False
            

    def render(self):
        self.play_button.render()
        self.quit_button.render()

        
        pos = (Game_Resources.DISPLAY_WIDTH/2, Game_Resources.DISPLAY_HEIGHT/4)
        self.game.render_text_to_display_centered("Cardungeon", pos, (200,100,200,255), 120)
