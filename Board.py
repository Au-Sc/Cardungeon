import Game_Objects
import Deck
import Cards

class Board(Game_Objects.RectangularGameObject):

    card_separation_offset = (10,10)
    card_size = (0,0)
    
    def __init__(self, game, i_columns, i_rows, i_card_size: (float,float)):
        Board.card_size = i_card_size
        w = Board.card_separation_offset[0] + i_columns*(Board.card_separation_offset[0] + i_card_size[0])
        h = Board.card_separation_offset[1] + i_rows*(Board.card_separation_offset[1] + i_card_size[1])
        self.COLUMNS = i_columns
        self.ROWS = i_rows
        super().__init__(game,0,0,w,h)
        self.grid = [[None for y in range(i_rows)] for x in range(i_columns)]
        self.game.game_state.board = self
        #variables for keeping track of important aspects
        self.attackers = 0

    def is_within_range(self, column, row):
        if ((column >= 0)and(column < self.COLUMNS)):
            if ((row >= 0)and(row < self.ROWS)):
                return True
        else:
            return False

    def get_cell_under_cursor(self):
        cell = (-1,-1)
        pos = tuple(self.game.mouse_pos)
        pos = (pos[0]-self.x, pos[1]-self.y)
        xmod = pos[0] % (Board.card_separation_offset[0]+Board.card_size[0])
        ymod = pos[1] % (Board.card_separation_offset[1]+Board.card_size[1])
        if (xmod > Board.card_separation_offset[0]
                and ymod > Board.card_separation_offset[1]
                and self.contains_point(self.game.mouse_pos)):
            cell = (int(pos[0] // (Board.card_separation_offset[0]+Board.card_size[0])),
                    int(pos[1] // (Board.card_separation_offset[1]+Board.card_size[1])))
        return cell

    def put(self, column, row, card):
        if not(self.is_within_range(column, row)):
            raise IndexError("Trying to access cell out of the Grid's bounds")
        
        if isinstance(card, Cards.Card):
            self.grid[column][row] = card;
            pos = self.get_position(column, row)
            card.x = pos[0]
            card.y = pos[1]

    def get_position(self, column, row):
        x = self.x + Board.card_separation_offset[0] + column*(Board.card_size[0] + Board.card_separation_offset[0])
        y = self.y + Board.card_separation_offset[1] + row*(Board.card_size[1] + Board.card_separation_offset[1])
        return (x,y)

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
            
            if (self.game.game_state.deck != None):
                while(lowest_empty != -1):
                    card = self.game.game_state.deck.draw_card()
                    if (card != None):
                        self.put(pos[0], lowest_empty, card)
                        lowest_empty -= 1
                    else:
                        break

    def action_tick(self):
        for x in range(self.COLUMNS):
            for y in range(self.ROWS):
                self.get(x,y).action_tick()

    def render(self):
        for x in range(self.COLUMNS):
            for y in range(self.ROWS):
                self.get(x,y).render()
    
    def update(self):
        for x in range(self.COLUMNS):
            for y in range(self.ROWS):
                self.get(x,y).update()
