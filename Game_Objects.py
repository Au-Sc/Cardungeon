import Game_Resources
from abc import ABC, abstractmethod

class GameObject(ABC):

    def __init__(self, game, i_x, i_y):
        self.game = game
        game.add_game_object(self)
        self.x = i_x
        self.y = i_y
    
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def update(self):
        pass

class RectangularGameObject(GameObject):

    def __init__(self, game, i_x, i_y, i_width, i_height):
        super().__init__(game, i_x, i_y)
        self.width = i_width
        self.height = i_height

    def get_center_global(self):
        return (self.x + (self.width/2), self.y + (self.height/2))

    def get_center_local(self):
        return (self.width/2, self.height/2)
    
    def set_position_centered(self, pos: (float, float)):
        self.x = pos[0] - (self.width/2)
        self.y = pos[1] - (self.height/2)

    def contains_point(self, point: (float, float)):
        if (point[0] >= self.x) and (point[0] <= self.x + self.width) and (point[1] >= self.y) and (point[1] <= self.y + self.height):
            return True
        else:
            return False

    
