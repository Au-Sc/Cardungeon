from abc import ABC, abstractmethod

class Game_object(ABC):
    def __init__(self, i_x, i_y):
        self.x = i_x
        self.y = i_y
    
    @abstractmethod
    def Draw(self, canvas):
        pass

    @abstractmethod
    def Update(self, game_data, deltatime):
        pass

class Rectangular_Game_object(Game_object):
    def __init__(self, i_x, i_y, i_width, i_height):
        super().__init__(i_x, i_y)
        self.width = i_width
        self.height = i_height

    def get_center_global(self):
        return (self.x + (self.width/2), self.y + (self.height/2))

    def get_center_local(self):
        return (self.width/2, self.height/2)
    
    def set_position_centered(self, pos: (float, float)):
        self.x = pos[0] - (self.width/2)
        self.y = pos[1] - (self.height/2)

class Clickable_Rect_Game_object(Rectangular_Game_object):
    def __init__(self, i_x, i_y, i_width, i_height):
        super().__init__(i_x, i_y, i_width, i_height)

    def got_clicked(self, pos: (float, float)):
        if (pos[0] >= self.x) and (pos[0] <= self.x + self.width) and (pos[1] >= self.y) and (pos[1] <= self.y + self.height):
            return True
        else:
            return False
