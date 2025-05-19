from Cards import Card
import Game_Objects

class Card_board(Game_Objects.Rectangular_Game_object):

    card_separation_offset = (10,10)
    
    def __init__(self, i_columns, i_rows):
        self.COLUMNS = i_columns
        self.ROWS = i_rows
        w = Card_board.card_separation_offset[0] + i_columns*(Card.card_img.get_width() + Card_board.card_separation_offset[0])
        h = Card_board.card_separation_offset[1] + i_rows*(Card.card_img.get_height() + Card_board.card_separation_offset[1])
        super().__init__(0,0,w,h)
        self.grid = [[None for y in range(i_rows)] for x in range(i_columns)]

    def is_within_size(self, column, row):
        if ((column >= 0)and(column <= self.COLUMNS)):
            if ((row >= 0)and(row <= self.ROWS)):
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
        for x in range(self.COLUMNS):
            for y in range(self.ROWS):
                if (isinstance(self.get(x,y), Card)):
                    self.grid[x][y].Draw(canvas)
    
    def Update(self, game_data, deltatime):
        for x in range(self.COLUMNS):
            for y in range (self.ROWS):
                self.grid[x][y].Update(game_data, deltatime)
