import Game_Resources
import Game_Objects
import Cards

class Player(Game_Objects.Game_object):
    def __init__(self):
        super().__init__(0,0)
        Game_Resources.game_player = self
    
    def attack(self, enemy):
        if isinstance(enemy, Cards.Enemy_Card):
            enemy.get_attacked(1)
    
    def Update(self, deltatime):
        #check for click
        if(Game_Resources.mouse_button_down):
            for x in range(Game_Resources.game_board.COLUMNS):
                for y in range(Game_Resources.game_board.ROWS):
                    obj = Game_Resources.game_board.grid[x][y]
                    if isinstance(obj, Cards.Enemy_Card):
                        if obj.contains_point(Game_Resources.mouse_pos):
                            self.attack(obj)
                            break
    
    def Draw(self, canvas):
        pass
