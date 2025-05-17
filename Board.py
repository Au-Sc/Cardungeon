from Cards import Card

class Card_Board:
    def __init__(self, i_width, i_height):
        self.WIDTH = i_width
        self.HEIGHT = i_height
        self.grid = [[None for y in range(i_height)] for x in range(i_width)]

    def is_within_size(self, column, row):
        if ((column >= 0)and(column <= self.WIDTH)):
            if ((row >= 0)and(row <= self.HEIGHT)):
                return True
        else:
            return False

    def put(self, column, row, card):
        if not(self.is_within_size(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if (isinstance(card, Card) ):
            self.grid[column][row] = card;

    def pop(self, column, row):
        if not(self.is_within_size(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        self.grid[column][row] = None

    def is_cell_empty(self, column, row):
        if not(self.is_within_size(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if (self.grid[column][row] is None):
            return True
        else:
            return False

    def get(self, column, row):
        if not(self.is_within_size(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        return self.grid[column][row]

    def Draw(self, canvas):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                if (isinstance(self.get(x,y), Card)):
                    self.grid[x][y].Draw(canvas)
    
    def Update(self, deltatime):
        pass
