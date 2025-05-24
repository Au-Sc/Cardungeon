import Game_Objects
import Deck
import Cards

class Card_board(Game_Objects.RectangularGameObject):

    card_separation_offset = (10,10)
    
    def __init__(self, game, i_columns, i_rows):
        self.COLUMNS = i_columns
        self.ROWS = i_rows
        super().__init__(game,0,0,0,0)
        self.grid = [[None for y in range(i_rows)] for x in range(i_columns)]
        self.game.board = self

    def is_within_range(self, column, row):
        if ((column >= 0)and(column <= self.COLUMNS)):
            if ((row >= 0)and(row <= self.ROWS)):
                return True
        else:
            return False

    def put(self, column, row, card):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if isinstance(card, Cards.Card):
            self.grid[column][row] = card;
            c_x = self.x + Card_board.card_separation_offset[0] + column*(card.width + Card_board.card_separation_offset[0])
            c_y = self.y + Card_board.card_separation_offset[1] + row*(card.height + Card_board.card_separation_offset[1])
            card.x = c_x
            card.y = c_y

    def pop(self, column, row):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        self.grid[column][row] = None

    def find_card(self, card):
        for x in range(self.COLUMNS):
            for y in range(self.ROWS):
                if (card is self.grid[x][y]):
                    return (x,y)
        return (-1,-1)

    def is_cell_empty(self, column, row):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if (self.grid[column][row] is None):
            return True
        else:
            return False

    def get(self, column, row):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        return self.grid[column][row]

    def discard(self, card):
        pos = self.find_card(card)
        if (pos != (-1,-1)):
            self.pop(pos[0],pos[1])
            lowest_empty = pos[1]
            for y in reversed(range(pos[1])):
                if not self.is_cell_empty(pos[0],y):
                    self.put(pos[0],lowest_empty, self.get(pos[0],y))
                    self.pop(pos[0],y)
                    lowest_empty -= 1
            
            if (self.game.deck != None):
                while(lowest_empty != -1):
                    card = self.game.deck.draw_card()
                    if (card != None):
                        self.put(pos[0], lowest_empty, card)
                        lowest_empty -= 1
                    else:
                        break

    def render(self):
        pass
    
    def update(self):
        pass
