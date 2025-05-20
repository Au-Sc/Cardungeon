import Game_Resources
from Cards import Card
import Game_Objects
import Deck

class Card_board(Game_Objects.Rectangular_Game_object):

    card_separation_offset = (10,10)
    
    def __init__(self, i_columns, i_rows):
        self.COLUMNS = i_columns
        self.ROWS = i_rows
        w = Card_board.card_separation_offset[0] + i_columns*(Card.card_img.get_width() + Card_board.card_separation_offset[0])
        h = Card_board.card_separation_offset[1] + i_rows*(Card.card_img.get_height() + Card_board.card_separation_offset[1])
        super().__init__(0,0,w,h)
        self.grid = [[None for y in range(i_rows)] for x in range(i_columns)]
        Game_Resources.game_board = self

    def is_within_range(self, column, row):
        if ((column >= 0)and(column <= self.COLUMNS)):
            if ((row >= 0)and(row <= self.ROWS)):
                return True
        else:
            return False

    def put(self, column, row, card):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if isinstance(card, Card):
            self.grid[column][row] = card;
            c_x = self.x + Card_board.card_separation_offset[0] + column*(card.width + Card_board.card_separation_offset[0])
            c_y = self.y + Card_board.card_separation_offset[1] + row*(card.height + Card_board.card_separation_offset[1])
            card.x = c_x
            card.y = c_y

    def pop(self, column, row):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        self.grid[column][row] = None

    def refill(self):
        if(Game_Resources.game_deck != None):
            #start on leftmost column, iterate to rightmost
            for x in range(self.COLUMNS):
                #now check bottom row in the actual column, and then we check the row above til we get to the top row
                for y in reversed(range(self.ROWS)):
                    #if the cell we're checking rn is empty...
                    if (self.grid[x][y] == None):
                        #...and we're not on the top row...
                        if (y != 0):
                            #check if any cell above has a card (reversed range with argument y (the row we're in rn) will generate a range from the row just above to the row at the very top)
                            for above_y in reversed(range(y)):
                                if self.grid[x][above_y] != None:
                                    #if so, move it to the cell we were checking
                                    aux = self.grid[x][above_y]
                                    self.pop(x,above_y)
                                    self.put(x,y,aux)
                                    break
                            #now if the cell we're in still doesn't has any card in it that means there is no card to bring down, so we should just draw a new one
                            if(self.grid[x][y] == None):
                                self.put(x, y, Game_Resources.game_deck.draw_card())
                        #...otherwise if we are on the top row we can't check for cards above, so we just draw a new one right away.
                        else:
                            self.put(x, y, Game_Resources.game_deck.draw_card())

    def find_card(self, card: Card):
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

    def Draw(self, canvas):
        pass
    
    def Update(self, deltatime):
        pass
